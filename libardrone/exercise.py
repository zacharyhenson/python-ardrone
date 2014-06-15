
from codeclubdrone import *
from pygame import *

drone = setup_drone()
bind_common_keys()

def fly_around():
    drone.takeoff()
    drone.land()

# The following means that whenever you press 'a',
# your function 'fly_around' above will get run.
bind_key(K_x, fly_around)

start_running_drone()
