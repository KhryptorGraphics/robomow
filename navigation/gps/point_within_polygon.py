#!/usr/bin/env python


# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.

def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        print p2x,p2y
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

if __name__=="__main__":
	import sys

	#polygon = ([0,0],[5,0],[5,5],[0,5])
	polygon = [(33.495296, -86.797129), (33.495273, -86.797107), (33.495276, -86.797016), (33.495354, -86.796978), (33.49537, -86.797029)]

	#33.4952309 -86.7971662 should = false (outside polygon)
	#33.4952980 -86.7970562 should = True (within polygon)

	print polygon, float(sys.argv[1]), float(sys.argv[2])
	print point_inside_polygon(float(sys.argv[1]),float(sys.argv[2]),polygon)


