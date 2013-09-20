'''
One listener is subscribed to a topic called 'rootTopic'.
One 'rootTopic' message gets sent. 
'''

import Image
from pubsub import pub
from pylab import imread
import cPickle as pickle
import numpy


# ------------ create a listener ------------------

def listener1(arg1, arg2=None):
	#print 'Function listener1 received:\n  arg1="%s"\n  arg2="%s"' % (arg1, arg2)
	img_rec = arg1
	#Image.fromarray(arg1).transpose(Image.FLIP_TOP_BOTTOM)
	print len(img_rec), type(img_rec)
	img1 = Image.fromarray(img_rec).transpose(Image.FLIP_TOP_BOTTOM)
	img1.show()
	

# ------------ register listener ------------------

pub.subscribe(listener1, 'rootTopic')

#------ create a function that sends a message ----

def doSomethingAndSendResult():
	fname = 'rec_image.jpg'
	#img = Image.open(filetosend)
	img = imread(fname)
	#print type(img), img.size, img.format, dir(img)
	# Pickle dictionary using protocol 0.
	#im = Image.fromarray(img).transpose(Image.FLIP_TOP_BOTTOM)
	#im.show()	
	print type(img), len(img)
	#p_img = pickle.dumps(img)	

	#print img.toString
	#img.show()
	#imshow(img)
	#f = open(filetosend, "rb")
	#img = f.read()
	#f.close()
	print 'lahdida... have result, publishing it via pubsub'
	#pub.sendMessage('rootTopic', arg1=123, arg2=dict(a='abc', b='def'))
	pub.sendMessage('rootTopic', arg1=img)

# --------- define the main part of application --------

if __name__ == '__main__':
	doSomethingAndSendResult()
