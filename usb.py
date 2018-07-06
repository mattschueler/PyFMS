#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes

# get the joystick file
dev = InputDevice('/dev/input/event3')

def event_result(event):
	ev_code = None
	ev_type = None
	ev_val = None
	# button was pressed
	if event.type == ecodes.EV_KEY:
		ev_type = 'button'
		if event.code == ecodes.BTN_TRIGGER:
			ev_code = '1'
		elif event.code == ecodes.BTN_THUMB:
			ev_code = '2'
		elif event.code == ecodes.BTN_THUMB2:
			ev_code = '3'
		elif event.code == ecodes.BTN_TOP:
			ev_code = '4'
		elif event.code == ecodes.BTN_TOP2:
			ev_code = 'L2'
		elif event.code == ecodes.BTN_PINKIE:
			ev_code = 'R2'
		elif event.code == ecodes.BTN_BASE:
			ev_code = 'L1'
		elif event.code == ecodes.BTN_BASE2:
			ev_code = 'R1'
		elif event.code == ecodes.BTN_BASE3:
			ev_code = 'select'
		elif event.code == ecodes.BTN_BASE4:
			ev_code = 'start'
		elif event.code == ecodes.BTN_BASE5:
			ev_code = 'L stick'
		elif event.code == ecodes.BTN_BASE6:
			ev_code = 'R stick'
		else:
			ev_code = 'other'
		if event.value == 0:
			ev_val = 'released'
		elif event.value == 1:
			ev_val = 'pressed'
		else:
			ev_val = 'other'
	#stick (or POV hat) was moved
	elif event.type == ecodes.EV_ABS:
		ev_type = 'axis'
		# thumbstick
		if event.code < 8:
			if event.code == ecodes.ABS_X:
				ev_code = 'left X'
			elif event.code == ecodes.ABS_Y:
				ev_code = 'left Y'
			elif event.code == ecodes.ABS_RX:
				ev_code = 'right X'
			elif event.code == ecodes.ABS_RZ:
				ev_code = 'right Y'
			else:
				ev_code = 'other'
		# pov hat
		else:
			if event.code == ecodes.ABS_HAT0X:
				ev_code = 'hat X'
			elif event.code == ecodes.ABS_HAT0Y:
				ev_code = 'hat Y'
			else:
				ev_code = 'other'
		ev_val = event.value
	else:
		ev_type = 'other'
	return [ev_type, ev_code, ev_val]

for event in dev.read_loop():
	# ignore these events because they happen all the time and aren't really important
	if event.type == ecodes.EV_KEY or (event.type == ecodes.EV_ABS and event.code != ecodes.ABS_Z):
		print(event_result(event))
