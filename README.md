# PyFMS
Field Management System written in Python that can use USB controllers to control LEGO Mindstorms NXT and EV3 bricks over a Bluetooth connection
The system was intended to be run on a Raspberry Pi that is Wifi and Bluetooth enabled. The device I used to develop and test the software was a Raspberry Pi 3B+. Other devices will probably work (provided they support *nix commands) but I make no guarantees.

# Required Libraries
python 3 (I used 3.5)
pybluez
bluez (5+)
bluez-utils

## Sources
The brick control portions of this project were heavily inspired by [nxt-python](https://github.com/Eelviny/nxt-python). This library only works for python 2, so I had to adapt it to fit my needs for the project in python 3
