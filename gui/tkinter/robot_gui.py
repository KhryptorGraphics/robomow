import Tkinter
import tkMessageBox
from PIL import Image, ImageTk
import time
from datetime import datetime
#from ThreadedBeatServer import *
import socket 

def check_heartbeat():

	#HOST = '127.0.0.1'                 # Symbolic name meaning the local host
	#PORT = 50008              # Arbitrary non-privileged port
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.bind((HOST, PORT)) 
	#next line spcifies how long in seconds to wait for a connection
	#s.settimeout(5.0)



	#print "listening..."
	#s.listen(1)
	#print "made connection..."

	reply = True
	UDP_IP="127.0.0.1"
	UDP_PORT=5005
	sock = socket.socket( socket.AF_INET, # Internet
		                  socket.SOCK_DGRAM ) # UDP
	sock.bind( (UDP_IP,UDP_PORT) )
	print "listening..."
	try:
		#next line spcifies how long in seconds to wait for a connection
		sock.settimeout(.3)
		#while True:
		data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
		print "received message:", data
		if data !="ACK": reply = False
	except IOError as detail:
   		print "connection lost", detail
		reply = False
	return reply


image = Image.open("temp.jpg")

top = Tkinter.Tk()
text1 = Tkinter.StringVar()
text1.set('Text')
heartbeat = Tkinter.StringVar()
heartbeat.set('NO HEARTBEAT')

i = 0
button_txt = i

def helloCallBack():
	global i
   	#tkMessageBox.showinfo( "Hello Python", "Hello World")
   	print "do some stuff"
   	i = i + 1
	B["text"]=i
   	#text1.set("New Text!")

	
def update_display():
		#global i
		text1.set( str(datetime.now()) )
		#top.update_idletasks()
		print "update called", i
		print "check heartbeat"
		#if check_heartbeat() == True: Label_HeartBeat["text"]='HEARTBEAT' 
		heart_check = check_heartbeat()
		if heart_check == True: heartbeat.set('HEARTBEAT')
		if heart_check == False: heartbeat.set('NO HEARTBEAT')
		top.update()

		top.after(50, update_display)


B = Tkinter.Button(top, text=button_txt, command = helloCallBack)
B2 = Tkinter.Button(top, text=button_txt, command = helloCallBack)
L1 = Tkinter.Label(top, textvariable=text1).pack()
Label_HeartBeat = Tkinter.Label(top, textvariable=heartbeat).pack()



photo = ImageTk.PhotoImage(image)
label = Tkinter.Label(image=photo)
label.image = photo # keep a reference!
label.pack()
B.pack()
B2.pack()
#first_run = False
if __name__== "__main__":
	update_display()
	#time.sleep(.01)
	print "hi"
	top.mainloop()
	print "out"

