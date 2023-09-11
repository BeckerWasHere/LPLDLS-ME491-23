#source /opt/ros/humble/setup.bash


import threading

import curses

from direct_control_shore.background_updates_render import background_updates_render

from direct_control_shore.handle_user_input import handle_user_input

#TODO move to its own class file
from direct_control_shore.handle_user_input import UserInterface

#TODO maybe separate into more files
from direct_control_shore.handle_connection_status import handle_connection_status
from direct_control_shore.handle_connection_status import background_connection_status_render

import rclpy

# # Initialize curses
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)
def main(stdscr):

	#ROS2
	rclpy.init(args=None)

	screen_view = UserInterface(stdscr)

	# screen_view.DEBUG()

	#TODO: rename
	commands_model_lock = threading.Lock()

	t_render_screen = threading.Thread(target = background_updates_render, args = [screen_view, commands_model_lock], daemon = True)
	t_render_screen.start()

	t_handle_connection_status = threading.Thread(target = handle_connection_status, args = [screen_view, commands_model_lock], daemon = True)
	t_handle_connection_status.start()

	t_handle_connection_status_background =  threading.Thread(target = background_connection_status_render, args = [screen_view, commands_model_lock], daemon = True)
	t_handle_connection_status_background.start()

	# for debuging
	# from direct_control_shore.handle_user_input_error_mode import UserInterface
	# t_user_input = threading.Thread(target = handle_user_input_error_mode, args = [screen_view, commands_model_lock], daemon = False)
	# t_user_input.start()

	t_user_input = threading.Thread(target = handle_user_input, args = [screen_view, commands_model_lock], daemon = False)
	t_user_input.start()

	t_user_input.join()


if __name__ == '__main__':

	# Run the program, the normal mode
	curses.wrapper(main)
	# srclpy.spin(minimal_publisher)


	# #crash mode, useful to debug
	# #Initialize curses:
	# stdscr = curses.initscr()
	# curses.noecho()
	# curses.cbreak()
	# stdscr.keypad(True)
	# main(stdscr)
	