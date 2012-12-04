import geopy
from geopy.distance import VincentyDistance

def get_dest_gps_cood(lat1, lon1, bearing, distance_in_meters):
	# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
	#lat1 = 53.32055555555556
	#lat2 = 53.31861111111111
	#lon1 = -1.7297222222222221
	#lon2 = -1.6997222222222223
	d = distance_in_meters / 1000.0
	b = bearing
	print d, b
	origin = geopy.Point(lat1, lon1)
	destination = VincentyDistance(kilometers=d).destination(origin, b)
	lat2, lon2 = destination.latitude, destination.longitude
	
	return lat2, lon2

if __name__== "__main__":
	lat1 = 53.32055555555556
	lon1 = -1.7297222222222221
	bearing = 270
	distance_in_meters = 10.0

	pos1 = get_dest_gps_cood(lat1, lon1, bearing, distance_in_meters/2.0)
	print "pos1 lat long:", pos1

	pos2 = get_dest_gps_cood(pos1[0], pos1[1], 0, distance_in_meters/2.0)
	print "pos2 lat long:", pos2
