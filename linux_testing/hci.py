import subprocess
import re

list_devices_cmd = 'sudo hcitool scan'.split(' ')

rfcomm_setup = None

with open('devices.txt', 'w') as devices:
	with open('error.txt', 'w+') as error:
		rfcomm_setup = subprocess.Popen(list_devices_cmd, stdout = devices, stderr = error)

if rfcomm_setup is not None:
	retcode = rfcomm_setup.wait()
	print(retcode)

with open('devices.txt', 'r') as devices:
	devices.readline()
	for line in devices:
		m = re.search('\s+(\S+)\s+(\S+)', line)
		print(m.groups())
