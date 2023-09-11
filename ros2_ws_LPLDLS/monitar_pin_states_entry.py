import threading

import curses

from monitor_pin_states.render_to_screen import handle_rendering_to_screen

from monitor_pin_states.listen_to_nano import handle_listener

from monitor_pin_states.render_pins import UserInterface

from shared.Model import Model

from shared.JetsonNanoPins import JetsonNanoPins

import rclpy

def main(stdscr):

	screen_view = UserInterface(stdscr)

	hardware_tracker = JetsonNanoPins()

	shared_model = Model(hardware_tracker)



	t_render_screen = threading.Thread(target = handle_rendering_to_screen, args = [shared_model, screen_view], daemon = True)
	t_render_screen.start()

	#ROS 2
	t_listen_to_nano = threading.Thread(target = handle_listener,  args = [shared_model], daemon = True)
	t_listen_to_nano.start()


	while True:
			# Get a key
		key = screen_view.stdscr.getch()
		# Exit if ESC is pressed
		if key == 27:
			curses.nocbreak()
			screen_view.stdscr.keypad(False)
			curses.echo()
			curses.endwin()
			break

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