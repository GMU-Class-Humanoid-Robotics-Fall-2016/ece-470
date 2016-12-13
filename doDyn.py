import time
import serial

def position(servoId, l_goal, h_goal):
	a_head 		= [0xff, 0xff]
	a_id 		= [servoId & 0xff] # [0x03]
	a_len 		= [0x05]
	a_cmd 		= [0x03] # Write Data
	a_address  	= [0x1e] # Goal Pos
	a_goal_l	= [l_goal] # Goal low byte
	a_goal_h	= [h_goal] # Goal high byte
	a_sum		= [~(a_id[0] + a_len[0] + a_cmd[0] + a_address[0] + a_goal_l[0] + a_goal_h[0]) & 0xff]  # get checksum
	the_out_list 	= a_head + a_id + a_len + a_cmd + a_address + a_goal_l + a_goal_h + a_sum
	the_out 	= bytearray(the_out_list)
	ser.write(the_out)
	pos = ((h_goal & 0x03) << 8) + l_goal
	pos = (pos * 300.0 / 1023.0) - 150.0
	print "Position Feedback: ", pos

def velocity(servoId, l_goal, h_goal, l_vel, h_vel):
	a_head 		= [0xff, 0xff]
	a_id 		= [servoId & 0xff] # [0x03]
	a_len 		= [0x07]
	a_cmd 		= [0x03] # Write Data
	a_address  	= [0x1e] # Goal Pos
	a_goal_l	= [l_goal] # Goal low byte
	a_goal_h	= [h_goal] # Goal high byte
	a_vel_l		= [l_vel] # Vel low byte
	a_vel_h		= [h_vel] # Vel high byte
	a_sum		= [~(a_id[0] + a_len[0] + a_cmd[0] + a_address[0] + a_goal_l[0] + a_goal_h[0] + a_vel_l[0] + a_vel_h[0]) & 0xff]  # get checksum
	the_out_list 	= a_head + a_id + a_len + a_cmd + a_address + a_goal_l + a_goal_h + a_vel_l + a_vel_h + a_sum
	the_out 	= bytearray(the_out_list)
	ser.write(the_out)
	pos = ((h_goal & 0x03) << 8) + l_goal
	pos = (pos * 300.0 / 1023.0) - 150.0
	print "Position Feedback: ", pos
	velD = h_vel >> 2
	vel = ((h_vel & 0x03) << 8) + l_vel
	vel = (vel * 114.0 / 1023.0)
	if velD:
		velD = velD * -1.0
	print "Velocity Feedback: ", vel

def torque(servoId, l_goal, h_goal, l_vel, h_vel, l_tor, h_tor):
	a_head 		= [0xff, 0xff]
	a_id 		= [servoId & 0xff] # [0x03]
	a_len 		= [0x09]
	a_cmd 		= [0x03] # Write Data
	a_address  	= [0x1e] # Goal Pos
	a_goal_l	= [l_goal] # Goal low byte
	a_goal_h	= [h_goal] # Goal high byte
	a_vel_l		= [l_vel] # Vel low byte
	a_vel_h		= [h_vel] # Vel high byte
	a_tor_l		= [l_tor] # Tor low byte
	a_tor_h		= [h_tor] # Tor high byte
	a_sum		= [~(a_id[0] + a_len[0] + a_cmd[0] + a_address[0] + a_goal_l[0] + a_goal_h[0] + a_vel_l[0] + a_vel_h[0] + a_tor_l[0] + a_tor_h[0]) & 0xff]  # get checksum
	the_out_list 	= a_head + a_id + a_len + a_cmd + a_address + a_goal_l + a_goal_h + a_vel_l + a_vel_h + a_tor_l + a_tor_h + a_sum
	the_out 	= bytearray(the_out_list)
	ser.write(the_out)
	pos = ((h_goal & 0x03) << 8) + l_goal
	pos = (pos * 300.0 / 1023.0) - 150.0
	print "Position Feedback: ", pos
	velD = h_vel >> 2
	vel = ((h_vel & 0x03) << 8) + l_vel
	vel = (vel * 114.0 / 1023.0)
	if velD:
		velD = velD * -1.0
	print "Velocity Feedback: ", vel
	torD = h_tor >> 2
	tor = ((h_tor & 0x03) << 8) + l_tor
	tor = (tor * 16.5 / 1023.0)
	if torD:
		torD = torD * -1.0
	print "Torque Feedback: ", tor

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=1000000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.open()
ser.isOpen()

while 1 :
    print "Choose valid values"
    print "p    - position"
    print "v    - position & velocity"
    print "t    - position, velocity & torque"
    print "exit - to leave the application"

    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    elif input == 'p':
		servoId = int(raw_input("ID: "))
		goal = float(raw_input("Goal: "))
		print "Valid degree range -150 to 150 degrees"
		if goal > -150.0 and goal < 150.0: 
			spos = int(((goal + 150.0) * 1023.0) / 300.0)
			l_goal = (spos & 0xff)
			h_goal = (spos & 0xff00) >> 8
			position(servoId, l_goal, h_goal)
		else:
			print "ERROR: \nValid degree range -150 to 150 degrees" 
    elif input == 'v':
		servoId = int(raw_input("ID: "))
		goal = float(raw_input("Degree: "))
		vel = float(raw_input("Velocity: "))
		print "Valid degree range -150 to 150 degrees"
		print "Valid velocity range 0 to 114 rpm"
		if (goal > -150.0 and goal < 150.0) and (vel > 0.0 and vel < 114.0):
			spos = int(((goal + 150.0) * 1023.0) / 300.0)
			l_goal = (spos & 0xff)
			h_goal = (spos & 0xff00) >> 8
			svel = int((vel * 1023.0) / 114.0)
			l_vel = (svel & 0xff)
			h_vel = (svel & 0xff00) >> 8
			velocity(servoId, l_goal, h_goal, l_vel, h_vel)
		else:
			print "ERROR: \nValid degree range -150 to 150 degrees \nValid velocity range 0 to 114 rpm"
    elif input == 't':
		servoId = int(raw_input("ID: "))
		goal = float(raw_input("Degree: "))
		vel = float(raw_input("Velocity: "))
		tor = float(raw_input("Torque: "))
		print "Valid degree range -150 to 150 degrees"
		print "Valid velocity range 0 to 114 rpm"
		print "Valid torque range 0 to 16.5"
		if (goal > -150.0 and goal < 150.0) and (vel > 0.0 and vel < 114.0) and (tor > 0.0 and tor < 16.5):
			spos = int(((goal + 150.0) * 1023.0) / 300.0)
			l_goal = (spos & 0xff)
			h_goal = (spos & 0xff00) >> 8
			svel = int((vel * 1023.0) / 114.0)
			l_vel = (svel & 0xff)
			h_vel = (svel & 0xff00) >> 8
			stor = int((tor * 1023.0) / 16.5)
			l_tor = (stor & 0xff)
			h_tor = (stor & 0xff00) >> 8
			torque(servoId, l_goal, h_goal, l_vel, h_vel, l_tor, h_tor)
		else:
			print "ERROR: \nValid degree range -150 to 150 degrees \nValid velocity range 0 to 114 rpm \nValid torque range 0 to 16.5"
    else:
		print "Choose valid values"
		print "p - position"
		print "v - position & velocity"
		print "t- position, velocity & torque"
		print "exit - to leave the application"

