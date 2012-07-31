#!/usr/bin/env python

import os
import time
import csv
import numpy as np

ifile  = open('gps_polygon.txt', "rb")
reader = csv.reader(ifile,  delimiter='\t')

line_info = []
gps_lat = []
gps_long = []
polygon = []

reader.next()
reader.next()
#read data from file into arrays
for row in reader:
	line_info.append(row)
	gps_lat.append(row[8])
	gps_long.append(row[9])
	temp = (float(row[8]), float(row[9]))
	polygon.append(temp)
	#print row
#print len(features)
#print line_info[0]
print gps_lat, gps_long
print;print;print
print polygon



