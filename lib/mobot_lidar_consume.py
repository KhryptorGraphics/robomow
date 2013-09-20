#!/usr/bin/python

import pika
import thread, time, sys, traceback
import cPickle as pickle	


''' USAGE:

	lidar = consume_lidar('lidar.1', 'localhost')
	while True:
		time.sleep(1)
		print lidar.data[1]
		print 'rpm speed:', lidar.speed_rpm
'''

class consume_lidar():
	def __init__(self, channel_name, host_ip):
		self.speed_rpm = 0
		self.data = []
		#-------------connection variables
		self.channel_name = channel_name
		self.host_ip = host_ip
		self.queue_name =  None
		self.connection = None
		self.channel = None
		#----------------------RUN
		self.run()
	
	def connect(self):
		self.connection =  pika.BlockingConnection(pika.ConnectionParameters(host=self.host_ip))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='mobot_data_feed',type='topic')	
		result = self.channel.queue_declare(exclusive=True)
		self.queue_name = result.method.queue
		binding_keys = self.channel_name
		self.channel.queue_bind(exchange='mobot_data_feed', queue=self.queue_name, routing_key=self.channel_name)

		
	def read_lidar(self):	
		while True:
			time.sleep(0.0001) # do not hog the processor power
			self.connect()
			for method_frame, properties, body in self.channel.consume(self.queue_name):
				#print "consuming"
				# Display the message parts
				temp_data = pickle.loads(body)		
				# Acknowledge the message
				self.channel.basic_ack(method_frame.delivery_tag)
				self.speed_rpm = temp_data[360]
				self.data = temp_data[:360]
				# Escape out of the loop after 10 messages
				#if method_frame.delivery_tag == 10:
				#	break

			# Cancel the consumer and return any pending messages
			#requeued_messages = self.channel.cancel()
			#print 'Requeued %i messages' % requeued_messages

			# Close the channel and the connection
			#self.channel.close()
			#self.connection.close()	
			
						
	def run(self):
		self.th = thread.start_new_thread(self.read_lidar, ())
	

if __name__== "__main__":

	lidar = consume_lidar('lidar.1', 'localhost')
	while True:
		time.sleep(1)
		print lidar.data[1]
		print 'rpm speed:', lidar.speed_rpm


                   

