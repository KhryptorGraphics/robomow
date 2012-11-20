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
		print (time.time()) - now
	except:
		print "could not grab webcam"
	return 

class send_video(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend     
		Thread.__init__(self)

	def run(self):
			print self.filetosend
			while True:
				snap_shot(self.filetosend)
				time.sleep(.1)
				#print "sending image"
				send_file(filetosend = self.filetosend)


def send_file(host="u1204vm.local", cport=9091, mport=9090, filetosend=""):
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
		
class send_sonar_data(Thread):
	def __init__(self):   
		#self.filetosend = filetosend     
		Thread.__init__(self)

	def run(self):
			#sonar = MaxSonar()
			while True:
				#sonar_data  = str(sonar.distances_cm())
				sonar_data = ""
				for i in range(1,6):
					sonar_data = sonar_data + "s"+str(i)+":"+ str(random.randint(28, 91))
				#sonar_data = "s1:61s2:33s3:45s4:87s5:91"
				print "sonar_data:", sonar_data
				f = open("sonar_data.txt", "w")
				f.write(sonar_data)
				f.close()
				time.sleep(.2)
				#print "sending image"
				send_file(filetosend="sonar_data.txt")


if __name__== "__main__":
	testmode = False
	if len(sys.argv) > 1:
		if sys.argv[1] == 'testmode':
				print 'starting in testing mode'
				testmode= True
				
	webcam1 = cv2.VideoCapture(0)
	video1 = send_video("snap_shot.jpg")
	video1.daemon
	video1.start()
	
	##start sonar
	if (testmode == False):
		sonar = send_sonar_data()
		sonar.daemon=True
		sonar.start()
	
	