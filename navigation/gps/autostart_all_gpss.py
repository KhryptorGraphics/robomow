
#this function will find and start all gps devices connected to linux computer

from subprocess import call
from identify_device_on_ttyport import *
import time

gps_list = find_usb_tty("067b","2303")

#gps_list = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
print "gps_list:", gps_list
print len(gps_list)
for n in range(len(gps_list)):
	start_gps = "gpsd "+gps_list[0]+" -S " + str(2947+n)
	print "start_gps:", start_gps
	returncode = call(start_gps, shell=True)
	time.sleep(2)
	print returncode

