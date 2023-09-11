import time
import curses
from shared.comm_info import get_pin_state_time_interval_s


#TODO impliment
def handle_connection_status(screen_view, commands_model_lock):

	# rclpy.init(args=None)

	connection_status_subscriber = ConnectionStatusSubscriber(screen_view, commands_model_lock)

	rclpy.spin(connection_status_subscriber)


def background_connection_status_render(screen_view, commands_model_lock):
	wait_time_s = get_pin_state_time_interval_s()

	while True:
	# backgound render if within time other wise wait
		commands_model_lock.acquire()
		within_wait_time: bool = screen_view.last_connection_time + wait_time_s > time.perf_counter()
		if screen_view.ready_to_render and not within_wait_time:
			status_color = 5; curses.init_pair(status_color, curses.COLOR_RED, curses.COLOR_BLACK)
			screen_view.top_bar_win.addstr(2, 0, "STATUS: ")
			screen_view.top_bar_win.addstr(2, 8, "NOT CONNECTED", curses.color_pair(status_color))
			screen_view.top_bar_win.refresh()
		commands_model_lock.release()
		time.sleep(wait_time_s)


import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class ConnectionStatusSubscriber(Node):
	def __init__(self, screen_view, commands_model_lock):
		super().__init__('Pin_States_Safety')
		self.subscription = self.create_subscription(
			String,
			'Pin_States_Safety',
			self.listener_callback,
			11)
		self.subscription  # prevent unused variable warning

		self.screen_view = screen_view
		self.commands_model_lock = commands_model_lock

		self.commands_model_lock.acquire()
		if self.screen_view.ready_to_render:
			status_color = 5; curses.init_pair(status_color, curses.COLOR_RED, curses.COLOR_BLACK)
			self.screen_view.top_bar_win.addstr(2, 0, "STATUS: ")
			self.screen_view.top_bar_win.addstr(2, 8, "NOT CONNECTED", curses.color_pair(status_color))
			self.screen_view.top_bar_win.refresh()
		self.commands_model_lock.release()

	
	def listener_callback(self, incoming_msg):
		self.commands_model_lock.acquire()
		if self.screen_view.ready_to_render:
			self.screen_view.last_connection_time = time.perf_counter()

			status_color = 5; curses.init_pair(status_color, curses.COLOR_GREEN, curses.COLOR_BLACK)
			self.screen_view.top_bar_win.addstr(2, 0, "STATUS: ")
			self.screen_view.top_bar_win.addstr(2, 8, "    CONNECTED", curses.color_pair(status_color))
			self.screen_view.top_bar_win.refresh()
		self.commands_model_lock.release()