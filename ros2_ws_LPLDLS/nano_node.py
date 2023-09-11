import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import json

import threading

import time


from shared.JetsonNanoPins import JetsonNanoPins



#global shared data
pin_lock = threading.Lock()
hardware_tracker = JetsonNanoPins()

time_interval_lock = threading.Lock()
time_interval_ms: float = 500





class DirectControlSubscriber(Node):

	def __init__(self):
		super().__init__('Direct_Contol_Nano')
		self.subscription = self.create_subscription(
			String,
			'Direct_Contol_Topic',
			self.listener_callback,
			10)
		self.subscription  # prevent unused variable warning

	#TODO: put the contents into a try and exeption(s) block
	def listener_callback(self, incoming_msg):
		# self.get_logger().info('I heard: "%s"' % msg.data)
		str_msg: str = incoming_msg.data
	

		parts = str_msg.split(":")
		str_type = parts[0].strip()

		if str_type == "PINS":

			global pins_lock
			global hardware_tracker
			global time_interval_lock
			global time_interval_ms

			pins_to_activate = json.loads(parts[1].strip())

			#for debuging
			counts = [0, 0]

			pin_lock.acquire()

			for pin_num in pins_to_activate:
				pin_num_int = int(pin_num)
				if pin_num_int in hardware_tracker.get_pins():

					bool_tracker = hardware_tracker.set_pin_use(pin_num_int, True)
					#TODO: Use Jetson Nano GPIO lib
					# time interval lock is not needed here, because this is the only thread capable of modifying it

					if bool_tracker:
						counts[0] += 1
					else:
						counts[1] += 1
					
			pin_lock.release()
			print(f"turned on {counts[0]} pins, kept {counts[1]} pins on")

		elif str_type == "TIME INTERVAL SET":
			global time_interval_ms
			old_time = time_interval_ms

			new_time_interval: float = float(str(parts[1].strip()))
			
			time_interval_lock.acquire()
			time_interval_ms = new_time_interval
			time_interval_lock.release()

			print(f"set the time form {old_time} ms to {time_interval_ms} ms")
		else:
			pass

#demon thread intended to turn off the pins and update the tracker if needed
def handle_pin_shut_offs():
	while True:
		
		
		pin_lock.acquire()
		time_interval_lock.acquire()

		global time_interval_ms
		global hardware_tracker

		for pin in hardware_tracker.get_pins():
			pin_is_turned_on = hardware_tracker.get_pin_use(pin)

			#multplication is easier than division for computers
			#TODO: get rid of magic number
			pin_is_old = ((time.perf_counter() - hardware_tracker.get_pin_mod_time(pin))*1000.0) >= time_interval_ms

			if not pin_is_turned_on:
				#for safety
				#TODO: use jetson nano GPIO lib to shut off pin
				pass
			elif pin_is_old:
				#TODO: use jetson nano GPIO lib to shut off pin
				hardware_tracker.set_pin_use(pin, False)
			else:
				pass

		#TODO: magic number
		sleep_time_ms = time_interval_ms - (time.perf_counter() - hardware_tracker.get_mod_time())*1000
		sleep_time_ms = min(abs(sleep_time_ms), time_interval_ms)

		pin_lock.release()
		time_interval_lock.release()
		

		time.sleep(sleep_time_ms / 1000)


from shared.comm_info import get_pin_state_time_interval_s
def report_on_state():
	time_to_wait_s: float = get_pin_state_time_interval_s()
	global hardware_tracker
	global pin_lock

	# ROS2
	Publisher = PinStatePublisher()

	while True:

		pin_lock.acquire()
		pins_set = set(hardware_tracker.get_pins())
		pin_lock.release()

		ROS2_msg: str = f"PINS: {list(pins_set)}"

		Publisher.single_call(ROS2_msg)

		time.sleep(time_to_wait_s)


from std_msgs.msg import String       

class PinStatePublisher(Node):
	def __init__(self):
		super().__init__('Pin_States_Safety')
		self.publisher_ = self.create_publisher(String, 'Pin_States_Safety', 11)

	def single_call(self, incoming_msg):
		msg = String()
		msg.data = incoming_msg #'Hello World: %d' % self.i
		self.publisher_.publish(msg)
		# self.get_logger().info('Publishing: "%s"' % msg.data)
		# self.i += 1



def main(args=None):

	rclpy.init(args=args)

	t_hardware_shut_off = threading.Thread(target = handle_pin_shut_offs, args = [], daemon = True)
	t_hardware_shut_off.start()

	t_report_on_state = threading.Thread(target = report_on_state, args = [], daemon = True)
	t_report_on_state.start()

	write_to_pins_subscriber = DirectControlSubscriber()

	rclpy.spin(write_to_pins_subscriber)


	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	write_to_pins_subscriber.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()