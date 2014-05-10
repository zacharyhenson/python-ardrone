Getting Started:
----------------

```python
>>> import libardrone
>>> drone = libardrone.ARDrone()
>>> # You might need to call drone.reset() before taking off if the drone is in
>>> # emergency mode
>>> drone.takeoff()
>>> drone.land()
>>> drone.halt()
```

The drone's property `image` contains always the latest image from the camera.
At present this is in the format of a numpy array with dimensions (width, height, 3).
This may change in future.
The drone's property `navdata` contains always the latest navdata.

There is also a simplified interface designed to match the standard Python
`turtle` module:

```python
import ardrone_turtle

takeoff()
forward(10)
left(180)
forward(10)
land()
```


Demo:
-----

There is also a demo application, `demo.py`, included which shows the video from the drone
and lets you remote-control the drone with the keyboard:

    RETURN      - takeoff
    SPACE       - land
    BACKSPACE   - reset (from emergency)
    a/d         - left/right
    w/s         - forward/back
    1,2,...,0   - speed
    UP/DOWN     - altitude
    LEFT/RIGHT  - turn left/right
    x           - run demo script (see 'School lesson', below)

Here is a [video] of the library in action:

  [video]: http://youtu.be/2HEV37GbUow

Turtle demo:
------------

A `demo2.py` script is included which uses the alternative turtle-compatible interface.

Repository:
-----------

The public repository is located here for the AR.Drone 1.0:

  git://github.com/venthur/python-ardrone.git

At present the AR.Drone 2.0 has a separate fork here:

  git://github.com/adetaylor/python-ardrone.git

Requirements:
-------------

This software was tested with the following setup:

  * Python 2.7.6
  * Unmodified AR.Drone firmware 2.0


License:
--------

This software is published under the terms of the MIT License:

  http://www.opensource.org/licenses/mit-license.php

School lesson plan:
-------------------

Funnily enough, flying robot drones seem to get kids interested in programming.
Here's a lesson plan which has been used with 10- and 11-year old kids in the UK.

  1. Hide the AR.Drone
  2. Show the [demo.py](libardrone/demo.py) `fly_around_school` code on a projector
  3. Ask the kids to talk through the code and explain what it does, one line at a time
  4. Show the drone ;-)
  5. Fire up `demo.py` and press `x`
  6. Be ready to press space when/if it comes close to any students. Seriously.
  7. The program _inevitably_ won't work out of the box.
  8. Debug it with the kids.
  9. Ask for proposed improvements (e.g. flying higher) and ask the kids to propose how to write it. Try it.

Step 9 is chaos but can easily fill an entire lesson.

One note: things work much better if the drone can see objects below it. A school hall floor or carpet has insufficient contrast. Lay books or coats on the floor.

More complex lessons, where the students write their own code, can be achieved by teaching the kids the standard `turtle` module and then converting to use the `ardrone_turtle` module included herein, which is supposed to have a roughly similar interface.

