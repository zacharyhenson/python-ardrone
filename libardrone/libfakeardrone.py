__author__ = 'adrian'

import numpy as np
from PIL import Image

"""
Like libardrone, but not real.
"""

class ARDrone(object):

    def __init__(self, is_ar_drone_2=False, hd=False):
        self.navdata = dict()
        self.navdata[0] = dict(zip(['ctrl_state', 'battery', 'theta', 'phi', 'psi', 'altitude', 'vx', 'vy', 'vz', 'num_frames'], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        self.speed = 0.2
        self.hd = hd
        if (self.hd):
            self.image_shape = (720, 1280, 3)
        else:
            self.image_shape = (360, 640, 3)
        self.overall_image = Image.open("/Users/adrian/Desktop/before.png")
        self.pos = [0, 0, 0]
        self.heading = 0

    def takeoff(self):
        """Make the drone takeoff."""
        self.pos[2] += 10

    def land(self):
        """Make the drone land."""
        self.pos[2] -= 10
        if self.pos[2] < 0:
            self.pos[2] = 0

    def hover(self):
        """Make the drone hover."""
        pass

    def move_left(self):
        """Make the drone move left."""
        pass

    def move_right(self):
        """Make the drone move right."""
        pass
        #self.at(at_pcmd, True, self.speed, 0, 0, 0)

    def move_up(self):
        """Make the drone rise upwards."""
        pass
        #self.at(at_pcmd, True, 0, 0, self.speed, 0)

    def move_down(self):
        """Make the drone decent downwards."""
        pass
        #self.at(at_pcmd, True, 0, 0, -self.speed, 0)

    def move_forward(self):
        """Make the drone move forward."""
        pass
        #self.at(at_pcmd, True, 0, -self.speed, 0, 0)

    def move_backward(self):
        """Make the drone move backwards."""
        pass
        #self.at(at_pcmd, True, 0, self.speed, 0, 0)

    def turn_left(self):
        """Make the drone rotate left."""
        pass
        #self.at(at_pcmd, True, 0, 0, 0, -self.speed)

    def turn_right(self):
        """Make the drone rotate right."""
        pass
        #self.at(at_pcmd, True, 0, 0, 0, self.speed)

    def reset(self):
        pass

    def trim(self):
        pass

    def set_speed(self, speed):
        """Set the drone's speed.

        Valid values are floats from [0..1]
        """
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
        pass

    def get_image(self):
        this_image = self.overall_image.rotate(-self.heading)
        altitude = self.pos[2]
        this_image = this_image.resize((self.overall_image.size[0] / altitude, self.overall_image.size[1] / altitude))
        this_image = this_image.crop(0, 0, self.pos[0], self.pos[1])
        _im = np.array(this_image).reshape(self.image_shape)
        return _im

    def get_navdata(self):
        return self.navdata
