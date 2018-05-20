from nxt import locator
import usb.backend.libusb1
from usb import core

backend = usb.backend.libusb1.get_backend(find_library=lambda x: './libusb/libusb-1.0-ms64.dll')

raw = False

if raw:
    # Here I try to do what the nxt library does manually, to no avail
    device = usb.core.find(idVendor=0x0694, idProduct=0x0002)
    device.set_configuration()
    ep_in, ep_out = device[0][(0,0)]

    device.write(ep_out, b'\x01\x9b', timeout=2000)
else:
    # How it is recommended to use nxt-python
    b = locator.find_one_brick(strict=False, debug=True)
