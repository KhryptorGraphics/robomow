

from math import *


def distance_and_bearings(lat1, lon1, lat2, lon2, start_altitude=0, dest_altitude=0):
	#GPS distance and bearing between two GPS points (Python recipe)
	#This code outputs the distance between 2 GPS points showing also the vertical and horizontal bearing between them. 
	#Haversine Formuala to find vertical angle and distance
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	#convert to meters
	#Base = Base * 1000 6367442.5
	Base = 6367442.5 * c
	Bearing = calcBearing(lat1, lon1, lat2, lon2)
	Bearing = round(degrees(Bearing), 2)
	distance = Base * 2 + dest_altitude * 2 / 2
	Caltitude = dest_altitude - start_altitude

	#Convertion from radians to decimals
	a = dest_altitude/Base
	b = atan(a)
	c = degrees(b)
	#Convert meters into Kilometers
	#distance = distance / 1000
	Base = round(Base,2)
	return Base, distance, c, Bearing

#Horisontal Bearing
def calcBearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)
    return atan2(y, x)


#Two Example GPS Locations
lat1 = 53.32055555555556
lat2 = 53.3206617415777
lon1 = -1.7297222222222221
lon2 = -1.7296909524757125
start_altitude = 0
dest_altitude = 10

H_Dist, distance, c, H_Bearing = distance_and_bearings(lat1, lon1, lat2, lon2, start_altitude, dest_altitude)


#Output the data
print("---------------------------------------")
print(":::::Auto Aim Directional Anntenna:::::")
print("---------------------------------------")
print("Horizontial Distance:", H_Dist,"meters")
print("   Vertical Distance:", distance,"km")
print("    Vertical Bearing:",c)
print(" Horizontial Bearing:",H_Bearing)
print("---------------------------------------")
input("Press <enter> to Exit")
