#!/usr/bin/env python
import sys, time
from threading import Thread
import numpy as np
import matplotlib.pyplot as P
from pylab import *
import Image
import cv
from maxsonar_class import *
import random

###########################################################

def PILtoCV_4Channel(PIL_img):
	cv_img = cv.CreateImageHeader(PIL_img.size, cv.IPL_DEPTH_8U, 4)
	cv.SetData(cv_img, PIL_img.tostring())
	return cv_img

###########################################################

def fig2img ( fig ):
	# put the figure pixmap into a numpy array
	buf = fig2data ( fig )
	w, h, d = buf.shape
	fig_return = Image.fromstring( "RGBA", ( w ,h ), buf.tostring( ) )
	buf = 0
	return fig_return

###########################################################

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf
###########################################################

def sonar_graph(ping_readings):
		
	# force square figure and square axes looks better for polar, IMO
	fig = figure(figsize=(6,6))
	ax = P.subplot(1, 1, 1, projection='polar')
	P.rgrids([28, 61, 91])
	ax.set_theta_zero_location('N')
	ax.set_theta_direction(-1)
	theta = 356
	angle = theta * np.pi / 180.0
	radii = [ping_readings[0]]
	width = .15
	bars1 = ax.bar(0, 100, width=0.001, bottom=0.0)
	#print "theta, radii, width: ", theta, radii, width
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	theta = 86
	angle = theta * np.pi / 180.0
	radii = [ping_readings[1]]
	width = .15
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')	
	theta = 176
	angle = theta * np.pi / 180.0
	radii = [ping_readings[2]]
	width = .15
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	theta = 266
	angle = theta * np.pi / 180.0
	radii = [ping_readings[3]]
	width = .15
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')

	pil_img = fig2img(fig)

	#print type(pil_img), pil_img
	sonar_image = PILtoCV_4Channel(pil_img)
	cv.ShowImage("Sonar", sonar_image )
	#cv.MoveWindow ('Sonar',50 ,50 )
	#time.sleep(.01)
	cv.WaitKey(10)

	#garbage cleanup
	fig.clf()
	P.close()
	return sonar_image


def sonar_display(sensor1):
	#global sensor1
	data  = str(sensor1.distances_cm())
	if len(data) > 1:
		#print "data=", data
		#s1_data = re.search('s1', data)
		#print s1_data.span()
		s1_data = data[(data.find('s1:')+3):(data.find('s2:'))]
		s2_data = data[(data.find('s2:')+3):(data.find('s3:'))]
		s3_data = data[(data.find('s3:')+3):(data.find('s4:'))]
		s4_data = data[(data.find('s4:')+3):(data.find('s5:'))]
		s5_data = data[(data.find('s5:')+3):(len(data)-1)]
		#print s1_data, s2_data, s3_data, s4_data, s5_data 
		s1_data = int(s1_data)
		if s1_data > 91: s1_data = 91
		if s1_data < 0: s1_data = 0
		sonar_graph(s1_data)	
		print s1_data
		#time.sleep(.01)

#t = Thread(target=sonar_display)
#t.start()

#sensor1 = MaxSonar()
#time.sleep(1)
#sonar_display(sensor1)
#time.sleep(1)

for i in range(1000):
	fake_data = []
	for i in range(5):
		fake_data.append(random.randint(28,91))
	print fake_data
	sonar_graph(fake_data)
	#time.sleep(.01)

