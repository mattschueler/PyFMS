import subprocess
import re

devices = []
bricks = []

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
setup.stdin.write(b'scan off\r\n')
setup.stdin.flush()

for device in devices:
	# ask if each device found is a NXT/EV3 and if it should be paired
	if input('Is {0} a brick? (y/N):'.format(device[1])) == 'y':
		bricks.append((device[0], device[1]))

for brick in bricks:
	print('Pairing {0}...'.format(brick[1]))
	# try to pair each device
	setup.stdin.write('pair {0}\r\n'.format(brick[0]).encode('utf-8'))
	setup.stdin.flush()
	code = False
	while setup.poll() is None:
		line = setup.stdout.readline().decode('utf-8')
		# did it ask for the PIN code
		if re.search('PIN code', line) is not None:
			# send 1234 as the PIN code
			setup.stdin.write(b'1234\r\n')
			setup.stdin.flush()
			code = True
			break
		# make sure that there were no errors
		elif re.search('Error', line) is not None:
			# print it out if there was
			print(line)
			break
	# if you sent the code
	if code:
		while setup.poll() is None:
			line = setup.stdout.readline().decode('utf-8')
			# if successful pairing, move on
			if re.search('Pairing successful', line) is not None:
				break
		print('Paired {0}'.format(brick[1]))
