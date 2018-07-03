import subprocess

ctl = list_devices_cmd = 'sudo bluetoothctl'.split(' ')

setup = subprocess.Popen(ctl, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

x = setup.communicate(input=b'scan on')
print(x)
