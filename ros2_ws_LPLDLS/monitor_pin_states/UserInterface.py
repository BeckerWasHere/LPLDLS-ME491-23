import curses

class UserInterface:
	def __init__(self, stdscr):
		self.stdscr = stdscr

		# Initialize colors
		curses.start_color()
		curses.use_default_colors()

		title_color = 1; curses.init_pair(title_color, curses.COLOR_BLUE, curses.COLOR_BLACK)

		self.title_bar_win = curses.newwin(1, 80, 0, 0)
		self.status_bar_win = curses.newwin(2, 80, 1, 0)
		self.main_content_win = curses.newwin(20, 80, 3, 0)
		self.stdscr.refresh()

		self.title_bar_win.addstr(0, 0, "Welcome to the pin state monitor", curses.color_pair(title_color))

		self.status_bar_win.addstr(0, 0, "STATUS BAR PLACE HOLER")
		self.status_bar_win.addstr(1, 0, "STATUS BAR PLACE HOLER")
		self.main_content_win.addstr(0, 0, "START OF CONTENT WINDOW")
		self.main_content_win.addstr(19, 0, "END OF CONTENT WINDOW")

		self.title_bar_win.refresh()
		self.main_content_win.refresh()
		self.status_bar_win.refresh()


		pin_activation_color = 2; curses.init_pair(title_color, curses.COLOR_GREEN, curses.COLOR_BLACK)

		connected_status_color = 3; curses.init_pair(title_color, curses.COLOR_GREEN, curses.COLOR_BLACK)
		not_connected_status_color = 4; curses.init_pair(title_color, curses.COLOR_RED, curses.COLOR_BLACK)

	def render_main_content(self, hardware_tracker):
		valid_pins_set = hardware_tracker.get_pins()

		count = 0
		for pin in valid_pins_set:

			#TODO: revisit this number
			if count > 40:
				break

			y_pos = count % 20
			x_pos = int(count / 10) * 20

			max_chars_pin_name: int = 10
			pin_name = f"PIN - {pin}"[:max_chars_pin_name]

			pin_is_on: bool = hardware_tracker.get_pin_use(pin)

			if pin_is_on:
				self.main_content_win.addstr(y_pos, x_pos, pin_name, curses.color_pair(pin_activation_color))
			else:
				self.main_content_win.addstr(y_pos, x_pos, pin_name)


			count += 1
		self.main_content_win.refresh()

	def render_status_bar(self, b_in_recent_contact):
		self.status_bar_win.addstr(0, 0, "STATUS: ")
		if b_in_recent_contact:
			self.status_bar_win.addstr(0, 8, "    CONNECTED", curses.color_pair(connected_status_color))
		else:
			self.status_bar_win.addstr(0, 8, "NOT CONNECTED", curses.color_pair(not_connected_status_color))
		self.status_bar_win.refresh()