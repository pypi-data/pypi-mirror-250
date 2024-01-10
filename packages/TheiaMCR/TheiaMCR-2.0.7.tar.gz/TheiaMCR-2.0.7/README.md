# Theia Technologies motor control board interface
[Theia Technologies](https://www.theiatech.com) offers a [MCR600 motor control board](https://www.theiatech.com/lenses/accessories/mcr/) for controlling Theia's motorized lenses.  This board controls focus, zoom, iris, and IRC filter motors.  It can be connected to a host comptuer by USB, UART, or I2C connection.  

# Features
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="20" height="20"/> The MCR600 board (and MCR400, MCR500 and others in the MCR series) has a proprietary command protocol to control and get information from the board.  The protocol is a customized string of up to 12 bytes which can be deciphered in the MCR600 [documentation](https://www.theiatech.com/lenses/accessories/mcr/).  For ease of use, Theia has developed this Python module to format the custom byte strings and send them to the board.  The user can request the focus motor to move 1000 steps for example.  The focusRel function will convert this request to the appropriate byte string and send it over USB connection to the MCR control board.  This will cause the lens motor to move 1000 steps.  

# Quick start
This module can be loaded into a Python program using pip.  
```pip install TheiaMCR```
Theia's motorized lens should be connected to the MCR600 board and the board should be connected to the host computer via USB connection thorugh a virtual com port.  
There are functions to initialize the board and motors and to control the movements (relative, absolute, etc).  The board must be initizlized first using the MCRControl __init__ function.  Then the motors must all be initialized with their steps and limit positions.  The init commands will create instances of the motor class for each motor which can be accessed by focus, zoom, and iris named instances.  

# Functions
## Initialization functions
- create a MCRControl class instance to initialize the board communications
- focusInit, zoomInit, irisInit: initialize the motors
- IRCInit: initialize the IR cut filter motor
## Motor movement functions
- IRCState: set the filter switch state to 0 or 1 
(For the following functions "motor" is replaced with "focus", "zoom" or "iris")
- motor.home: send the motor to the home position and set the current step number
- motor.moveAbs: move the motor to an absolute step number after sending it to home first.  Moving to absolute step < 0 is possible if setRespectLimits(False).  
- motor.moveRel: move by a relative number of steps
## Information and setting functions
- MCRBoard.readFWRevision: read board firmware revision
- MCRBoard.readBoardSN: read board serial number
- motor.setMotorSpeed: set the motor speed in pulses per second (pps)
- motor.setRespectLimits: turn on or off the home position limit stops for focus and zoom

# Important variables
Each motor has these variables available
- motor.currentStep: current motor step number
- motor.currentSpeed: current motor speed in pulses per second (pps)
- motor.maxSteps: maximum number of steps for the full range of movement
- motor.PIStep: photointerrupber limit switch step position (within the full range of movement).  After sending the motor to home, the current step will be set to this PIStep number.  

# License
Theia Technologies BSD license
Copyright 2023 Theia Technologies

# Contact information
For more information contact: 
Mark Peterson at Theia Technologies
[mpeterson@theiatech.com](mailto://mpeterson@theiatech.com)

# Revision
v.2.0.7