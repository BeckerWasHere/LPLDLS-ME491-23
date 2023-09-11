import abc


class ViewScreen():#metaclass=abc.ABCMeta):
	HORIZONTAL_SIZE = 80
	VERTICAL_SIZE = 20

	# @abc.abstractmethod
	def __init__(self):
		raise Exception("Default Constructor Not Allowed")
		pass

	# @abc.abstractmethod
	def __init__(self, stdscr):
		    # Initialize colors

		pass

	# @abc.abstractmethod
	def render_start(self):
		pass

	# @abc.abstractmethod
	def render_title(self):
		pass

	# @abc.abstractmethod
	def render_status_bar(self):
		pass

	# @abc.abstractmethod
	def render_content(self):
		pass

class DirectControlViewScreen(ViewScreen):

	def render_start(self):
		pass

	def render_title(self):
		pass

	def render_status_bar(self):
		pass

	def render_content(self):
		pass


def test_block(stdscr):

	#V = DirectControlViewScreen()
	return

import curses
curses.wrapper(test_block)






def generate_command_screen(stdscr):
	stdscr.clear()
	command_x_pos.clear()
	command_y_pos.clear()

	vertical_offset = 1
	total_space_per_name = 30

	vertical_count = 0
	horizontal_count = 0
	for name in command_pins.keys():
		if (vertical_count + vertical_offset > 10): #max_screen_height
			horizontal_count += total_space_per_name
			vertical_count = 0
		command_x_pos[name] = horizontal_count
		command_y_pos[name] = vertical_count + vertical_offset
		if (vertical_count + vertical_offset <= 10):
			vertical_count += 1



    
    #generate block of command names
	for name in command_pins.keys():
		stdscr.addstr(command_y_pos[name], command_x_pos[name], name)

	stdscr.addstr(0, 40, f"time interval: {time_interval_ms} ms")
	return