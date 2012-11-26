#!/usr/bin/python


from gps_functions import *
from math import *

#Two Example GPS Locations 
lat1 = 53.32055555555556
lat2 = 53.31861111111111
lon1 = -1.7297222222222221
lon2 = -1.6997222222222223
#lat1 = 33.466582
#lon1 =  -86.824076

#peru
#lat2 = -14.087724
#lon2 = -75.763532

#lat2 = 33.466582
#lon2 =  -86.8240652425



Aaltitude = 2000
Oppsite  = 20000

a = [lat1, lon1]
b = [lat2, lon2]
print "lldistance(a, b) in meters: ", lldistance(a, b)

print "haversine(lon1, lat1, lon2, lat2) in meters: ",  haversine(lon1, lat1, lon2, lat2)*1000

print "calculate_distance(lat1, lon1, lat2, lon2): ", calculate_distance(lat1, lon1, lat2, lon2)

#print "points2distance(a,  b):", points2distance(a, b)


bearing = degrees(calcBearing(lat1, lon1, lat2, lon2))
bearing = (bearing + 360) % 360

print "calcBearing(lat1, lon1, lat2, lon2):", bearing 

print "distance.distance(ne, cl).meters" , geopyDistance(lat1, lon1, lat2, lon2)

print "bearing2(lat1, lon1, lat2, lon2):", bearing2(lat1, lon1, lat2, lon2) 

destLat, destLong = destination_coordinates(lat1, lon1, bearing , calculate_distance(lat1, lon1, lat2, lon2))

print "destination_coordinates(lat1, lon1, 55, 12):", destLat, destLong
print "bearing2(lat1, lon1, destLat, destLong):", bearing2(lat1, lon1, destLat, destLong) 
print "meters_to_feet(meters)", meters_to_feet(calculate_distance(lat1, lon1, lat2, lon2))

