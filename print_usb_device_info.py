# This program will query your system for a list of all USB devices currently
# connected. It will attempt to print out the name, vendor id, product id, USB
# bus number, and the USB port number if it can, and will print empty strings
# if it cannot find a piece.

import usb.core
from ctypes import *
import os
from tabulate import tabulate
import operator

# Import the libusb DLL file
dll_name = 'libusb-1.0-ms64.dll'
dllpath = os.path.join(os.path.abspath('./libusb'),dll_name)
libusb = CDLL(dllpath)

# Find all USB devices connected
devices = usb.core.find(find_all=1)

headers = ['Product','Vendor ID','Product ID','Bus','Port']
rows = []
for device in devices:
    try:
        rows.append([device.product, device.idVendor, device.idProduct, device.bus, device.port_number])
    except ValueError:
        print('ValueError')
    except NotImplementedError:
        print('NotImplementedError')

# This sorts the devices by bus number and port number
rows.sort(key=operator.itemgetter(3,4))
print(tabulate(rows, headers=headers))
