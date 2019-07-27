from subprocess import *
from bluetooth import *
from BtSocket import BtSocket
import re

pinfilename = '/home/pi/pincodes.txt'

class BluetoothManager():
    def __init__(self):
        self.agent_process = None

    def add_device_with_pin(self, mac_addr, pincode):
        if not self.is_device_in_file(mac_addr):
            with open(pinfilename, 'a+') as pinfile:
                pinfile.write('{0} {1}\n'.format(mac_addr, pincode))

    def is_device_in_file(self, mac_addr):
        with open (pinfilename, 'r') as pinfile:
            for line in pinfile:
                if re.search(re.escape(mac_addr), line):
                    return True
        return False

    def run_bluetooth_agent(self):
        cmd = ['bt-agent', '-p', pinfilename]
        self.agent_process = Popen(cmd, stdout=DEVNULL)

    def pair_with_device(self, mac_addr):
        sock = BtSocket(mac_addr)
        sock.connect()
        sock.send(b"\x01\x9B")
        print(sock.recv())

    def add_new_device(self, mac_addr):
        self.add_device_with_pin(mac_addr, "1234")
        self.run_bluetooth_agent()
        self.pair_with_device(mac_addr)
        self.agent_process.kill()
        self.agent_process = None

    def list_all_devices(self):
        return discover_devices(lookup_names=True)

    def remove_device(self, mac_addr):
        cmd = ['bt-device', '-r', mac_addr]
        rem_process = Popen(cmd, stdout=DEVNULL)
        rem_process.wait()
