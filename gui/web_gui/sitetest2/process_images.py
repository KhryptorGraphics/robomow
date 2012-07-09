#!/usr/bin/env python

import os
from img_processing_tools import *
import Image 
import time
import sys
import cv

root_path = "/home/lforet/images"
num_of_classes = 2

if __name__=="__main__":
	
	if len(sys.argv) < 2:
		data_filename = 'mower_image_data.csv'
		for x in range(num_of_classes):
			if x == 0: 
				classID = 1
				path = root_path + "/class1"
			if x == 1:
				classID = -1
				path = root_path + "/class2"
			
			###########################
			#process class 1 files (mowable)
			###########################
			count = 0
			for subdir, dirs, files in os.walk(path):
				count = len(files)
			if count > 0:
				if x == 0:
					###########################
					# delete data file and write header
					f_handle = open(data_filename, 'w')
					f_handle.write(str("classid, lbp, i3_histogram, rgb_histogram, sum_I3, sum2_I3, median_I3, avg_I3, var_I3, stddev_I3, rms_I3"))
					f_handle.write('\n')
					f_handle.close()
	 
				print "Files to Process: ", count
				for subdir, dirs, files in os.walk(path):
					for file in files:
						filename1= os.path.join(path, file)
						if x == 0: print "Processing images: CLASS 1 (MOWABLE)"
						if x == 1: print "Processing images: CLASS -1 (NON-MOWABLE)"
						print "Processing file: ", filename1
						img = Image.open(filename1)
						if len(img.getbands()) == 3:
							if img.size[0] <> 640 or img.size[1] <> 480:
								print "Image is not right size. Resizing image...."
								img = img.resize((640, 480))
								print "Resized to 640, 480"
								#cv.WaitKey()
							cv_image = PILtoCV(img)
							cv.ShowImage("Image", cv_image)
							cv.MoveWindow ('Image',50 ,50 )
							cv.WaitKey(100)
							#strg = "python show_histogram.py " + filename1
							#print strg
							#os.system(strg);
							plot_rgb_histogram(img)
							time.sleep(.1)
							cv_image2 = cv.LoadImage('histogram.png')
							cv.ShowImage("RGB Histogram", cv_image2)
							cv.MoveWindow ('RGB Histogram',50 ,580 )
							cv.WaitKey(100)
							#cv.WaitKey()
							time.sleep(.2)

							WriteMeterics(img, classID, data_filename)
							
						else:
							print "image not valid for processing: ", filename1
							time.sleep(3)
						print

	if len(sys.argv) > 1:
		classID = 0
		data_filename = 'sample_image_data.csv'
		###########################
		# delete data file and write header
		f_handle = open(data_filename, 'w')
		f_handle.write(str("classid, lbp, i3_histogram, rgb_histogram, sum_I3, sum2_I3, median_I3, avg_I3, var_I3, stddev_I3, rms_I3"))
		f_handle.write('\n')
		f_handle.close()

		filename1= sys.argv[1]
		print 'writing sample image stats to file: ', data_filename
		print "Processing file: ", filename1
		img = Image.open(filename1)
		if len(img.getbands()) == 3:
			if img.size[0] <> 640 or img.size[1] <> 480:
				print "Image is not right size. Resizing image...."
				img = img.resize((640, 480))
			print "Resized to 640, 480"
			cv_image = PILtoCV(img)
			cv.ShowImage("Image", cv_image)
			cv.MoveWindow ('Image',50 ,50 )
			cv.WaitKey(100)
			time.sleep(.2)
			WriteMeterics(img, classID, data_filename)
			#time.sleep(1)
		else:
			print "image not valid for processing: ", filename1
			time.sleep(5)
		print


