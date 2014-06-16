#
# CodeClub AR.Drone exercise

from codeclubdrone import *
from pygame import *

# The next line gives you an 'object'
# An 'object' is something a bit like a Sprite in Scratch
# except that you might not be able to see it on the screen.
# It's something that might have variables and scripts
# attached to it. In this case, the object represents
# an AR.Drone flying robot.
# Except: if you say 'True' not 'False' you'll instead get
# a pretend AR.Drone simulator. When you're ready to try
# your program on a real AR.Drone, just change True to False.

drone = setup_drone(True)

# You'll want a set of keys to be usable to control your
# drone. This sets up those keys. You can skip this if you
# want, but you'll probably regret it.
bind_common_keys()

# Fill whatever you want into this function.
def fly_around():
    drone.takeoff()
    drone.land()

# The following means that whenever you press 'x',
# your function 'fly_around' above will get run.
# label="Fly around" means you'll get a nice reminder
# on the screen stating what the key does.
bind_key(K_x, fly_around, label="Fly around")

# After you've set everything up, call start_running_drone()
# to get it cracking!
start_running_drone()
