from shared.JetsonNanoPins import JetsonNanoPins

import threading

import time

#TODO: RENAME
def handle_listener(shared_model):

	rclpy.init(args=None)

	NanoPinStateSubscriber

	pass


import rclpy
from rclpy.node import Node

from std_msgs.msg import String
class NanoPinStateSubscriber(Node):
	def __init__(self, shared_model):
		super().__init__('Pin_States_Safety')
		self.subscription = self.create_subscription(
			String,
			'Pin_States_Safety',
			self.listener_callback,
			11)
		self.subscription  # prevent unused variable warning


		self.shared_model = shared_model

		pass

	
	def listener_callback(self, incoming_msg):
		self.shared_model.lock.acquire()
		#clear all pins

		#add only pins that are in use

		#set connection status to true and update time

		self.shared_model.lock.release()
		pass