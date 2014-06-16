__author__ = 'adrian'

import numpy as np
from PIL import Image
import traceback
import math
import threading
import time
import os

def radians(degrees):
    return 0.0174532925 * (degrees % 360)

"""
Like libardrone, but not real.
"""

class ARDrone(object):

    def __init__(self, is_ar_drone_2=False, hd=False):
        self.navdata = dict()
        self.navdata[0] = dict(zip(['ctrl_state', 'battery', 'theta', 'phi', 'psi', 'altitude', 'vx', 'vy', 'vz', 'num_frames'], [0, 100, 0, 0, 0, 0, 0, 0, 0, 0]))
        self.speed = 0.1
        self.hd = hd
        if (self.hd):
            self.image_shape = (720, 1280, 3)
        else:
            self.image_shape = (360, 640, 3)
        image_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fakeground.png")
        self.overall_image = Image.open(image_filename).convert("RGB") # remove alpha
        self.pos = [self.overall_image.size[0]/2, self.overall_image.size[1]/2]
        self.delta_pos = [0, 0, 0]
        self.lock = threading.Lock()
        self.thread = None
        self.rotation_to_do = 0
        self.landing = self.cease_flying = False

    def navdata_lock(self):
        class AcquiredLock(object):
            def __init__(self, lock):
                self.lock = lock

            def __enter__(self):
                self.lock.acquire()

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.lock.release()

        return AcquiredLock(self.lock)

    def takeoff(self):
        """Make the drone takeoff."""
        if self.thread is not None:
            return
        if self.navdata[0]['altitude'] > 0 or self.landing:
            return
        self.navdata[0]['altitude'] = 0.1
        self.delta_pos = [0,0,1.0]
        self.cease_flying = False
        self.thread = threading.Thread(target=ARDrone.do_flying, args=(self,))
        self.thread.daemon = True
        self.thread.start()

    def do_flying(self):
        while (not self.cease_flying) and (self.navdata[0]['altitude'] > 0):
            with self.navdata_lock():
                for i in range(2):
                    self.pos[i] += self.delta_pos[i]
                self.navdata[0]['altitude'] += self.delta_pos[2]
                if self.navdata[0]['altitude'] < 0:
                    self.navdata[0]['altitude'] = 0
                    self.landing = False
                if self.rotation_to_do != 0:
                    self.navdata[0]['psi'] += (self.speed * self.rotation_to_do)
                    self.navdata[0]['psi'] = (self.navdata[0]['psi'] % 360)
                if self.landing:
                    self.navdata[0]['altitude'] = -self.speed
                print("Pos is %f,%f" % (self.pos[0], self.pos[1]))
            time.sleep(0.1)
        self.thread = None

    def land(self):
        """Make the drone land."""
        with self.navdata_lock():
            if self.navdata[0]['altitude'] == 0 or self.landing:
                return
            self.landing = True

    def hover(self):
        """Make the drone hover."""
        with self.navdata_lock():
            self.delta_pos = [0, 0, 0]
            self.rotation_to_do = 0

    def _do_motion(self, angle):
        with self.navdata_lock():
            self.delta_pos[0] += 20 * self.speed * math.sin(radians(self.navdata[0]['psi'] + angle))
            self.delta_pos[1] += 20 * self.speed * math.cos(radians(self.navdata[0]['psi'] + angle))

    def move_left(self):
        """Make the drone move left."""
        self._do_motion(90)

    def move_right(self):
        """Make the drone move right."""
        self._do_motion(-90)

    def move_forward(self):
        """Make the drone move forward."""
        self._do_motion(0)

    def move_backward(self):
        """Make the drone move backwards."""
        self._do_motion(180)

    def move_up(self):
        """Make the drone rise upwards."""
        with self.navdata_lock():
            self.delta_pos[2] = self.speed

    def move_down(self):
        """Make the drone decend downwards."""
        with self.navdata_lock():
            self.delta_pos[2] = -self.speed

    def turn_left(self):
        """Make the drone rotate left."""
        with self.navdata_lock():
            self.rotation_to_do -= 5

    def turn_right(self):
        """Make the drone rotate right."""
        with self.navdata_lock():
            self.rotation_to_do += 5

    def reset(self):
        self.cease_flying = True
        if self.thread:
            self.thread.join()

    def trim(self):
        pass

    def set_speed(self, speed):
        """Set the drone's speed.

        Valid values are floats from [0..1]
        """
        with self.navdata_lock():
            self.speed = speed

    def configure_multisession(self, session_id, user_id, app_id, config_ids_string):
        pass

    def set_session_id (self, config_ids_string, session_id):
        pass

    def set_profile_id (self, config_ids_string, profile_id):
        pass

    def set_app_id (self, config_ids_string, app_id):
        pass

    def set_video_bitrate_control_mode (self, config_ids_string, mode):
        pass

    def set_video_bitrate (self, config_ids_string, bitrate):
        pass

    def set_video_channel(self, config_ids_string, channel):
        pass

    def set_max_bitrate(self, config_ids_string, max_bitrate):
        pass

    def set_fps (self, config_ids_string, fps):
        pass

    def set_video_codec (self, config_ids_string, codec):
        pass

    def halt(self):
        self.reset()

    def get_image(self):
        try:
            with self.navdata_lock():
                altitude = self.navdata[0]['altitude']
                psi = self.navdata[0]['psi']
            if altitude == 0:
                return np.zeros(self.image_shape)
            fraction_of_image_we_want_to_see = 1
            if altitude < 100:
                fraction_of_image_we_want_to_see = altitude / 100.0
            desired_width = int(self.overall_image.size[0] * fraction_of_image_we_want_to_see)
            desired_ratio = float(self.image_shape[0]) / self.image_shape[1]
            desired_height = int(desired_width * desired_ratio)
            # First crop to twice the area which we want to see
            this_image = self.overall_image
            this_image = this_image.crop((int(self.pos[0] - desired_width), int(self.pos[1] - desired_height),
                                                  int(self.pos[0] + desired_width), int(self.pos[1] + desired_height)))
            # Then rotate
            rotation_angle = int(psi % 360)
            if rotation_angle != 0:
                this_image = this_image.rotate(-rotation_angle)
            # Now shrink again
            mid_x = this_image.size[0] / 2
            mid_y = this_image.size[1] / 2
            this_image = this_image.crop((int(mid_x - desired_width/2), int(mid_y - desired_width/2),
                                          int(mid_x + desired_height/2), int(mid_y + desired_height/2)))
            this_image = this_image.resize((self.image_shape[1], self.image_shape[0]))
            # Rotate 90 due to weird AR.Drone rotation
            this_image = this_image.rotate(270) # clockwise!
            # PIL images result in arrays which are (rows, columns, rgb)
            # PyGame (and thus libardrone users) expect (x, y, rgb)
            # Hence we need to swap first two axes
            _im = np.array(this_image).swapaxes(0, 1)
            return _im
        except:
            traceback.print_exc()

    def get_navdata(self):
        return self.navdata

    def get_image_shape(self):
        return (self.image_shape[0], self.image_shape[1])