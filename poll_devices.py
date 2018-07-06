# this is basically just the first section of bt_setup

import subprocess
import re
import csv

devices = []

# open bluetoothctl process
setup = subprocess.Popen('sudo bluetoothctl'.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# turn on agent and start scan
setup.stdin.write(b'agent on\r\nscan on\r\n')
setup.stdin.flush()
try:
	print('Searching for devices...')
	# poll the stdout of the process
	while setup.poll() is None:
		line = setup.stdout.readline().decode('utf-8')
		# if new device is discovered
		if re.search('NEW', line) is not None:
			#get the MAC address and name of the device
			dev_match = re.search('Device (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) (\w+)', line)
			# make sure that there was actually a MAC addr and name found
			if dev_match is not None:
				addr = dev_match.group(1)
				name = dev_match.group(3)
				# add a new device to the list
				devices.append((addr,name))
				print('Found {0}'.format(name))
except:
	# if there is an error, stop
	# this allows you to Ctrl-C to continue on
	print('Search stopped')
setup.stdin.write(b'exit\r\n')
setup.stdin.flush()

# create a csv file of all devices to keep track of the ones you have found
with open('devices.csv', 'w') as dev_file:
	writer = csv.writer(dev_file)
	for device in devices:
		writer.writerow([device[0],device[1]])
