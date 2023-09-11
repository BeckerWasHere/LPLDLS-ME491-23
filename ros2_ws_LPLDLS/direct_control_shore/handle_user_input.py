# import threading
import time
import curses

from direct_control_shore.UserInterface import UserInterface
from shared.JetsonNanoPins import JetsonNanoPins


def handle_user_input_error_mode(screen_view, commands_model_lock):
	try:
		handle_user_input(screen_view, commands_model_lock)
	except Exception as e:
		global error_message_set
		error_message_set.add("Error caught" + str(e))


def handle_user_input(screen_view, commands_model_lock):

	# ROS2
	Publisher = DirectControlPublisher()

	# to make sure the shore and nano are synched upon start of direct control 
	ROS2_msg = f"time interval set: {screen_view.time_interval_ms}"
	Publisher.single_call(ROS2_msg)

	valid_keys_set = set()

	while True:
		# Get a key
		key = screen_view.stdscr.getch()

		commands_model_lock.acquire()

		#for the purposes of debuging
		if key == ord("F"):
			screen_view.DEBUG()

		# Exit if ESC is pressed
		elif key == 27:
			curses.nocbreak()
			screen_view.stdscr.keypad(False)
			curses.echo()
			curses.endwin()
			break

		# for processing the commands from the file
		elif key == ord("!"):
			#attempt to build the dictionaries and render the screen, else render the most detailed error possible
			if screen_view.generate_dictionaries_from_json():
				screen_view.generate_command_screen()
				# screen_view.DEBUG()
				screen_view.render_time_interval_change(0)
				# screen_view.DEBUG()
				valid_keys_set = screen_view.command_keys.keys()

		elif (key == ord("+") or key == ord("=")):
			
			screen_view.render_time_interval_change(25)
			
			# ROS2
			ROS2_msg = f"TIME INTERVAL SET: {screen_view.time_interval_ms}"
			Publisher.single_call(ROS2_msg)


		elif (key == ord("-") or key == ord("_")):
			screen_view.render_time_interval_change(-25)

			# ROS2
			ROS2_msg = f"TIME INTERVAL SET: {screen_view.time_interval_ms}"
			Publisher.single_call(ROS2_msg)	

		elif str(chr(key)) in valid_keys_set:
			if screen_view.handle_key_hit(str(chr(key))):
				command_name = screen_view.command_keys[str(chr(key))]

				# ROS 2 stuff
				ROS2_msg = f"PINS: {screen_view.command_pins[command_name]}"
				Publisher.single_call(ROS2_msg)
				pass


		else:
			pass
				


			

		commands_model_lock.release()



#TODO move to another file
import rclpy
from rclpy.node import Node

from std_msgs.msg import String       

class DirectControlPublisher(Node):
	def __init__(self):
		super().__init__('Direct_Contol_Shore')
		self.publisher_ = self.create_publisher(String, 'Direct_Contol_Topic', 10)

	def single_call(self, incoming_msg):
		msg = String()
		msg.data = incoming_msg #'Hello World: %d' % self.i
		self.publisher_.publish(msg)
		# self.get_logger().info('Publishing: "%s"' % msg.data)
		# self.i += 1