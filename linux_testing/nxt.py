import bluetooth
import serial
import traceback
import time

s = serial.Serial(port='/dev/rfcomm0', baudrate=9600, bytesize=8, timeout=3.0, write_timeout=3.0)

try:
	s.write(b'\x02\x00\x01\x9b')
	print(s.readline())
except:
	traceback.print_exc()

s.close()
