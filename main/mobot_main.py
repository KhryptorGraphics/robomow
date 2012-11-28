#!/usr/local/bin/python

from PIL import Image, ImageTk
import time
from datetime import datetime
import socket 
import cv2
from threading import *
import sys
from maxsonar_class import *
import random
from robomow_motor_class_arduino import *


hhh = 0
file_lock = False


def snap_shot(filename):
	#capture from camera at location 0
	now = time.time()
	global webcam1
	try:
		#have to capture a few frames as it buffers a few frames..
		for i in range (5):
			ret, img = webcam1.read()		 
		#print "time to capture 5 frames:", (time.time()) - now
		cv2.imwrite(filename, img)
		img1 = Image.open(filename)
		img1.thumbnail((320,240))
		img1.save(filename)
		#print (time.time()) - now
	except:
		print "could not grab webcam"
	return 

def send_file(host, cport, mport, filetosend):
	#global file_lock
	file_lock = True
	#print "file_lock", file_lock
	try:       
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((host, cport))
		cs.send("SEND " + filetosend)
		print "sending file", filetosend
		cs.close()
	except:
		print "cs failed"
		pass
	time.sleep(0.1)
	try:
		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((host, mport))
		f = open(filetosend, "rb")
		data = f.read()
		f.close()
		ms.send(data)
		ms.close()
	except:
		print "ms failed"
		pass
	#file_lock = False
	#print "file_lock", file_lock
		
		
'''
def send_data(host="u1204vm.local", cport=9091, mport=9090, datatosend=""):
	try:       
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((host, cport))
		cs.send("SEND " + filetosend)
		cs.close()
	except:
		pass
	time.sleep(0.05)
	try:
		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((host, mport))
		f = open(filetosend, "rb")
		data = f.read()
		f.close()
		ms.send(data)
		ms.close()
	except:
		pass
'''	
class send_video(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend     
		Thread.__init__(self)

	def run(self):
			#global file_lock, hhh
			print self.filetosend
			while True:
				snap_shot(self.filetosend)	
				send_file(host="u1204vm.local", cport=9090, mport=9091,filetosend=self.filetosend)
				time.sleep(.01)
							
class send_sonar_data(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend
		self.sonar_data = "" 
		self.max_dist = -1
		self.min_dist = -1   
		self.min_sensor = -1
		self.max_sensor = -1 
		Thread.__init__(self)

	def run(self):
			#global file_lock, hhh
			sonar = MaxSonar()
			
			while True:
				self.sonar_data = ""
				self.max_dist = -1
				self.min_dist = -1 
				self.min_sensor = -1
				self.max_sensor = -1
				#
				#below 2 lines are for test purposes when actual US arent sending data
				#for i in range(1,6):
				#	sonar_data = sonar_data + "s"+str(i)+":"+ str(random.randint(28, 91))

				data = str(sonar.distances_cm())
				self.sonar_data = []
				sonar_data_str1 = ""
				if len(data) > 1:
					self.sonar_data.append(int(data[(data.find('s1:')+3):(data.find('s2:'))]))
					self.sonar_data.append(int(data[(data.find('s2:')+3):(data.find('s3:'))]))
					self.sonar_data.append(int(data[(data.find('s3:')+3):(data.find('s4:'))]))
					self.sonar_data.append(int(data[(data.find('s4:')+3):(data.find('s5:'))]))
					self.sonar_data.append(int(data[(data.find('s5:')+3):(len(data)-1)]))
					self.max_dist = max(self.sonar_data)
					self.min_dist = min(self.sonar_data)
					self.min_sensor = self.sonar_data.index(self.min_dist)
					self.max_sensor = self.sonar_data.index(self.max_dist)
					#sonar_data_str1 = "".join(str(x) for x in self.sonar_data)
					#print sonar_data_str1
					#print data
					f = open("sonar_data.txt", "w")
					f.write(data)
					f.close()
					send_file(host="u1204vm.local", cport=9092, mport=9093,filetosend=self.filetosend)
				time.sleep(.01)
			print "out of while in sonar"


def move_mobot(themove):
	if (themove == "foward"):
		motor1.forward(100)
		time.sleep(.2)
		print motor1.motor1_speed, motor1.motor2_speed
	if (themove == "reverse"):
		motor1.reverse(100)
		time.sleep(.2)
		print motor1.motor1_speed, motor1.motor2_speed
	if (themove == "left"):
		motor1.left(100)
		time.sleep(.2)
		print motor1.motor1_speed, motor1.motor2_speed
	if (themove == "right):
		motor1.right(100)
		time.sleep(.2)
		print motor1.motor1_speed, motor1.motor2_speed
	if (themove == "stop"):
		motor1.stop()
		time.sleep(.2)
		print motor1.motor1_speed, motor1.motor2_speed
	

if __name__== "__main__":
	testmode = False
	if len(sys.argv) > 1:
		if sys.argv[1] == 'testmode':
				print 'starting in testing mode'
				testmode= True

				
	webcam1 = cv2.VideoCapture(0)


	video1 = send_video("snap_shot.jpg")
	video1.daemon=True
	video1.start()
	#video1.join()
	
	
	##start sonar
	if (testmode == False):
		sonar = send_sonar_data("sonar_data.txt")
		sonar.daemon=True
		sonar.start()
		#sonar.join()

	motor = robomow_motor()
	print "motor.isConnected:", motor.isConnected

	while True:
		if (sonar.max_dist > 0):
			move = ""
			print "......................"
			print "sonar_data: ", sonar.sonar_data
			print "max dist: ", sonar.max_dist, sonar.max_sensor
			print "min_dist: ", sonar.min_dist, sonar.min_sensor
			if sonar.max_sensor == 0: move = "foward"
			if sonar.max_sensor == 1: move = "right"
			#if sonar.max_sensor == 2: move = "reverse"
			if sonar.max_sensor == 3: move = "left"
			print "suggest moving: ", move
			#move_mobot(move)

		time.sleep(1)
	print "stopped"


