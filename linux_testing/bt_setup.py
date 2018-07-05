import subprocess
import re

bricks = []

setup = subprocess.Popen('sudo bluetoothctl'.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
setup.stdin.write(b'agent on\r\nscan on\r\n')
setup.stdin.flush()
while setup.poll() is None:
	line = setup.stdout.readline().decode('utf-8')
	if re.search('NEW', line) is not None:
		dev_match = re.search('Device (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}) (\w+)', line)
		if dev_match is not None:
			addr = dev_match.group(1)
			name = dev_match.group(3)
			if input('Is {0} a brick? (y/N):'.format(name)) == 'y':
				bricks.append((addr, name))
			if input('Find another brick? (y/N):') != 'y':
				break

for brick in bricks:
	setup.stdin.write('pair {0}\r\n'.format(brick[0]).encode('utf-8'))
	setup.stdin.flush()
	while setup.poll() is None:
		line = setup.stdout.readline().decode('utf-8')
		if re.search('PIN code', line) is not None:
			setup.stdin.write(b'1234\r\n')
			setup.stdin.flush()
			break
	while setup.poll() is None:
		line = setup.stdout.readline().decode('utf-8')
		if re.search('Pairing successful', line) is not None:
			break
	print('Paired {0}'.format(brick[1]))
