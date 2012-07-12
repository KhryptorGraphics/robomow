#!/usr/bin/env python

import os
from img_processing_tools import *
import Image, ImageDraw
import time
import sys
import cv
from PIL import ImageStat
import numpy as np

def classifiy_section(img):
	#class_ID: 1=grass, 2=non-mowable, 3=unknown
	class_ID = 2
	#print img[0], img[1], img[2]
	#print "class_ID", class_ID
	#if (img[0] > 65 and img[0] < 115) and (img[1] > 70 and img[1] < 135) and (img[2] < 85):	class_ID = 1
	#if img[0] > 82 and img[1] > 85 and img[2] > 72:	class_ID = 2	
	
	rb_sum = img[0] + img[2]
	g_sum = img[1]
	if img[1] > 26: class_ID=1

	#if img[1] < 15 and img[2] > 5 : class_ID=2
	print "rgb: ", img, "class_ID: ", class_ID
	return class_ID


def rgb2I3 (img):
	"""Convert RGB color space to I3 color space
	@param r: Red
	@param g: Green
	@param b: Blue
	return (I3) integer 
	"""
	img_width, img_height = img.size
	#make a copy to return
	returnimage = Image.new("RGB", (img_width, img_height))
	imagearray = img.load()
	for y in range(0, img_height, 1):					
		for x in range(0, img_width, 1):
			rgb = imagearray[x, y]
			i3 = ((2*rgb[1])-rgb[0]-rgb[2]) / 2
			#print rgb, i3
			returnimage.putpixel((x,y), (0,i3,0))
	return returnimage



def subsection_image(pil_img, sections, visual):
	sections = sections /4
	print "sections= ", sections
	fingerprint = []

	# - -----accepts image and  number of sections to divide the image into (resolution of fingerprint)
	# ---------- returns a subsectioned image classified by terrain type
	img_width, img_height = pil_img.size
	print "image size = img_wdith= ", img_width, "  img_height=", img_height, "  sections=", sections
	if visual == True:
		cv_original_img1 = PILtoCV(pil_img)
		cv.ShowImage("Original",cv_original_img1 )
		cv.MoveWindow("Original", ((img_width)+100),50)
	pil_img = rgb2I3 (pil_img)
	#cv.WaitKey()
	temp_img = pil_img.copy()
	xsegs = img_width  / sections
	ysegs = img_height / sections
	print "xsegs, ysegs = ", xsegs, ysegs 
	for yy in range(0, img_height-ysegs+1 , ysegs):
		for xx in range(0, img_width-xsegs+1, xsegs):
			print "Processing section =", xx, yy, xx+xsegs, yy+ysegs
			box = (xx, yy, xx+xsegs, yy+ysegs)
			print "box = ", box
			cropped_img1 = pil_img.crop(box)
			I3_mean =   ImageStat.Stat(cropped_img1).mean
			I3_mean_rgb = (int(I3_mean[0]), int(I3_mean[1]), int(I3_mean[2]))
			print "I3_mean: ", I3_mean
			sub_ID = classifiy_section(I3_mean_rgb)
			fingerprint.append(sub_ID)
			if visual == True:
				cv_cropped_img1 = PILtoCV(cropped_img1)
				cv.ShowImage("Fingerprint",cv_cropped_img1 )
				cv.MoveWindow("Fingerprint", (img_width+100),50)
				if sub_ID == 1: I3_mean_rgb = (50,150,50)
				if sub_ID == 2: I3_mean_rgb = (150,150,150)
				if sub_ID == 3: I3_mean_rgb = (0,0,200)
				ImageDraw.Draw(pil_img).rectangle(box, (I3_mean_rgb))
				cv_img = PILtoCV(pil_img)
				cv.ShowImage("Image",cv_img)
				cv.MoveWindow("Image", 50,50)
				cv.WaitKey(5)
				#time.sleep(.05)
	#print "FINGERPRINT: ", fingerprint
	#cv.WaitKey()
	return fingerprint

###########################################################


if __name__=="__main__":

 
#	if len(sys.argv) < 4:
#		print "******* Requires 3 image files of the same size."
#		print "This program will return the angle at which the second is in relation to the first. ***"
#		sys.exit(-1)

	try:
		#img1 = cv.LoadImage(sys.argv[1])
		#frame = grab_frame(1)
		img1 = Image.open(sys.argv[1])
		#img1 = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
		#img1 = CVtoGray(frame)
		#cv.WaitKey()
		#img1 = CV_enhance_edge(img1)
		#cv.WaitKey()
		#img2 = cv.LoadImage(sys.argv[1],cv.CV_LOAD_IMAGE_GRAYSCALE)
		#img3 = cv.LoadImage(sys.argv[2],cv.CV_LOAD_IMAGE_GRAYSCALE)
	except:
		print "******* Could not open image files *******"
		sys.exit(-1)
	print len (sys.argv)
	if len(sys.argv) == 2:
		resolution = 32
	else:
		resolution = int(sys.argv[2])
	image_fingerprint = np.array(subsection_image(img1, resolution, True))
	print "FINGERPRINT: ",image_fingerprint
	print 'len(image_fingerprint):', len(image_fingerprint)
	#image_fingerprint.reshape(((image_fingerprint/2), 2))
	print image_fingerprint 
	step = len(image_fingerprint)/ (resolution/4)
	print "step =", step
	a = []
	b = []
	for x in range (0, len(image_fingerprint), step):
		#print x
		for y in range(0, step/2):
			#print x,y
			a.append(image_fingerprint[(x+y)])
			b.append(image_fingerprint[(x+(step/2)+y)])
			#print a
			#print b

	direction = sum(a)-sum(b)
	print "leftside-rightside:", direction 
	if direction > 0: print "grass on right"
	if direction < 0: print "grass on left"
	cv.WaitKey()

