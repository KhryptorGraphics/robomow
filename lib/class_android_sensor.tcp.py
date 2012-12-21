from threading import Thread
import time
import sys 
import socket
import math

def read_line(s):
    ret = ''

    while True:
        c = s.recv(1)

        if c == '\n' or c == '':
            break
        else:
            ret += c

    return ret
    

class android_sensor_tcp(Thread):
	def __init__(self, port):
		self.host = ''  
		self.port = port  # Arbitrary non-privileged port
		self.socket = None   
		self.light = 0.0,
		self.accuracy = 0.0
		self.xforce = 0.0
		self.yforce = 0.0
		self.zforce = 0.0
		self.xMag = 0.0
		self.yMag = 0.0
		self.zMag = 0.0
		self.pitch = 0.0
		self.roll= 0.0
		self.azimuth = 0.0
		self.heading = 0.0
		Thread.__init__(self)
			
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		#print "listening..."
		self.socket.listen(1)
		try:
			print "waiting to accept.."
			conn, addr = self.socket.accept()
			print "accepted connection from client.."
			while conn <> "":
				self.socket.listen(1)
				#print time.time()
				#print s.gettimeout()
				#print 'Connected by', addr
				#data = conn.recv(1024)
				data = read_line(conn)
				data1 = data.split(',')
				#print data1
				try:
					self.light = float(data1[1])
					self.accuracy = float(data1[2])
					self.xforce = float(data1[3])
					self.yforce = float(data1[4])
					self.zforce = float(data1[5])
					self.xMag = float(data1[6])
					self.yMag = float(data1[7])
					self.zMag = float(data1[8])
					self.pitch = float(data1[9])
					self.roll = float(data1[10])
					self.azimuth = float(data1[11])
					self.heading = math.degrees(self.azimuth)
					if self.heading < 0: self.heading = self.heading + 360
					#print "heading:", round(self.heading,2)
				except:
				    pass
				#time.sleep(.1) 
		
		except IOError as detail:
			print "connection lost", detail

		try:
			print "closing Socket"
			self.socket.close()
		except NameError as detail:
			print "No socket to close", detail

if __name__== "__main__":

	android_sensor = android_sensor_tcp(8095)
	android_sensor.daemon=True
	android_sensor.start()
	while True:
		print round(android_sensor.heading, 2)
		time.sleep(.1)
	del android_sensor

