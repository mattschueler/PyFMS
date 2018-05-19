# This program allows to you read the input data from the controller whenever it is run.
# This code could go in a loop, but since it prints everything out to the screen
# but this would very quickly fill the terminal window, so I opted not to do this
# for this simple test program

import usb.core
import usb.backend.libusb1
from ctypes import *
import os
import time
import copy

# Maps the data bytes to something like (data[i]&j)>>k to extract individual buttons, sticks, hats, etc
device_name = 'DragonRise_Inc.-Generic__USB__Joystick'
with open('controller_configs/{0}.cfg'.format(device_name)) as f:
    data_map = eval(f.read())

# Takes the mapping read from the file and uses it to find the values for each
# stick, hat, or button
def mapDataToVars(data, mapping):
    values = copy.deepcopy(mapping)
    for elem in mapping:
        map = mapping[elem]
        values[elem] = (data[map['index']]&map['mask'])>>map['shift']
    return values

# Wraps the DLL backend to PyUSB
backend = usb.backend.libusb1.get_backend(find_library=lambda x: './libusb/libusb-1.0-ms64.dll')
# Get a list of all the controllers with this vendor and product id
# Note: this is specific to the controller I used, you will have to find which
# numbers are used for your controllers
devices = list(usb.core.find(idVendor=121, idProduct=6, find_all=1))
# Initialize the controllers found
map(lambda device: device.set_configuration(), devices)
# Get the reading endpoints for USB communication
readEPs = [device[0][(0,0)][0] for device in devices]

final_str = ""
for i in range(len(devices)):
    # Read data from the connection
    data = devices[i].read(readEPs[i].bEndpointAddress,readEPs[i].wMaxPacketSize,100)
    # Map this data using the loaded configuration
    mapped_data = mapDataToVars(data, data_map)
    final_str += str(mapped_data) + '\n'
print(final_str)
