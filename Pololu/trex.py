#!/usr/bin/python
import serial
import time

class TReX:
    fwd = 1
    rvs = 2
    speed_normal = 127
	
    cmd_prefix = chr(0x86)
	
    cmd_accelerate = 0xE0

    lastAction = ''
	
    def __init__(self,pname='/dev/ttyS2',baudrate=19200):
        self.port = serial.Serial(pname)
        self.port.baudrate= baudrate

    def basic_action(self, thisAction):
	if self.lastAction != thisAction:
		if thisAction == "f":
			print "/\ Forwards"
			self.forwards()
		elif thisAction == "b":
			print "\/ Backwards"
			self.backwards()
		elif thisAction == "l":
			print "<< Left"
			self.left()
		elif thisAction == "r":
			print ">> Right"
			self.right()
		else:
			print ">< Stopped"
			self.stop()
		self.lastAction = thisAction


    def forwards(self):
        self.accelerate_to(self.fwd, self.fwd, self.speed_normal, self.speed_normal)
			
    def backwards(self):
        self.accelerate_to(self.rvs, self.rvs, self.speed_normal, self.speed_normal)
			
    def left(self):
        self.accelerate_to(self.fwd, self.rvs, self.speed_normal, self.speed_normal)
			
    def right(self):
        self.accelerate_to(self.rvs, self.fwd, self.speed_normal, self.speed_normal)

    def stop(self):
        self.accelerate_to(self.fwd, self.fwd, 0, 0)
			
    def accelerate_to(self, left_dir, right_dir, left_power, right_power):
        self.port.write(self.cmd_prefix+chr(self.cmd_accelerate | left_dir*4 | right_dir) + chr(left_power) + chr(right_power))
 

#p = TReX()

#while ( 1 ):
#        p.basic_action('r')
#        time.sleep (1)
PORT = "/dev/ttyUSB0"

#if len(sys.argv) > 1:
#    PORT = sys.argv[1]

ser = serial.Serial(PORT, 19200, timeout=1)

print ser.portstr,
print ser.baudrate,
print ser.bytesize,
print ser.parity,
print ser.stopbits
while 1:
    ser.write (chr(0x81))      # write a string
    print 'waiting on response..'
    s = ser.readline()
    ser.write (chr(0x82))
    s = ser.readline()
    time.sleep(1)
ser.close() 
print s

