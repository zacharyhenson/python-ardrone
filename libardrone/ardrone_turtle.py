import libardrone
import time

drone = libardrone.ARDrone(True) # always assumes AR.Drone 2.0
drone.speed = 0.1
drone.reset()
time.sleep(0.1)
drone.trim()

def takeoff():
    print "takeoff()"
    drone.takeoff()

def land():
    print "land()"
    drone.land()

def forward(distance):
    print "forward(%d)" % (distance)
    for x in range(distance):
        drone.move_forward()
        time.sleep(0.3)

def backward(distance):
    print "backward(%d)" % (distance)
    for x in range(distance):
        drone.move_backward()
        time.sleep(0.3)

def right(degrees):
    print "right(%d)" % (degrees)
    def dorightturn():
        drone.turn_right()
    __turn(degrees, dorightturn)

def left(degrees):
    print "left(%d)" % (degrees)
    def doleftturn():
        drone.turn_left()
    __turn(degrees, doleftturn)

def __turn(degrees, action):
    current_rotation = __get_rotation()
    desired_rotation = (current_rotation + degrees) % 360
    print "Current rotation is " + str(current_rotation)
    print "We want to turn to " + str(desired_rotation)
    while (current_rotation > (desired_rotation+5) or current_rotation < (desired_rotation - 5)):
        print "Current rotation is "+str(current_rotation)+", turning further..."
        action()
        current_rotation = get_rotation()

def __get_rotation():
    return (drone.navdata.get(0, dict()).get('psi', 0)) % 360

