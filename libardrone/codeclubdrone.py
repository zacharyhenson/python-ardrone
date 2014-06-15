__author__ = 'adrian'

import pygame
import pygame.surfarray

import pygame.transform
import time
import libardrone
import libfakeardrone
from threading import Thread

drone = None
FAKE = True
running = True
keys = dict()
screen = None
clock = None


def setup_drone():
    global screen, drone, clock
    pygame.init()
    W, H = 640, 480
    screen = pygame.display.set_mode((W, H))
    if FAKE:
        drone = libfakeardrone.ARDrone(True)
    else:
        drone = libardrone.ARDrone(True)
    drone.reset()
    clock = pygame.time.Clock()
    time.sleep(2.0)
    drone.trim()
    return drone


def get_drone():
    if drone is None:
        raise Exception("Please call setup_drone() first")
    return drone


def bind_key(key, function):
    keys[key] = function


def bind_common_keys():
    bind_key(pygame.K_ESCAPE, lambda: get_drone().reset())
    bind_key(pygame.K_RETURN, lambda: get_drone().takeoff())
    bind_key(pygame.K_SPACE, lambda: get_drone().takeoff())
    bind_key(pygame.K_BACKSPACE, lambda: get_drone().reset())
    bind_key(pygame.K_w, lambda: get_drone().move_forward())
    bind_key(pygame.K_s, lambda: get_drone().move_backward())
    bind_key(pygame.K_a, lambda: get_drone().move_left())
    bind_key(pygame.K_d, lambda: get_drone().move_right())
    bind_key(pygame.K_UP, lambda: get_drone().move_up())
    bind_key(pygame.K_DOWN, lambda: get_drone().move_down())
    bind_key(pygame.K_LEFT, lambda: get_drone().turn_left())
    bind_key(pygame.K_RIGHT, lambda: get_drone().turn_right())

    def set_speed(speed):
        get_drone().speed = speed

    bind_key(pygame.K_0, lambda: set_speed(1.0))
    for i in range(9):
        bind_key(pygame.K_1 + i, lambda: set_speed(i/10.0))


def start_running_drone():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYUP:
                drone.hover()
            elif event.type == pygame.KEYDOWN:
                if event.key in keys:
                    action = keys[event.key]
                    t = Thread(target=action)
                    t.daemon = True
                    t.start()
        try:
            # print pygame.image
            pixelarray = drone.get_image()
            if pixelarray is not None:
                surface = pygame.surfarray.make_surface(pixelarray)
                rotsurface = pygame.transform.rotate(surface, 270)
                screen.blit(rotsurface, (0, 0))
            # battery status
            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print("Shutting down...")
    drone.halt()
    print("Ok.")

def stop():
    running = False
