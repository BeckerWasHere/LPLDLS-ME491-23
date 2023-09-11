import time
import curses

from shared.JetsonNanoPins import JetsonNanoPins

class UserInterface:

	command_file_error_message: str = None

	#command to pins
	command_pins = {} #TODO: rename to commands_to_pins_dict
	#key to command name
	command_keys = {} #TODO: rename to keys_to_commands_dict
	#the last write time
	command_in_use = {} #TODO: rename to commands_to_write_times_dict

	max_screen_width: int = 80
	max_screen_height: int = 25
	command_x_pos = {}
	command_y_pos = {}


	time_interval_ms: float = 500
	min_time_interval_ms: float = 25
	max_time_interval_ms: float = 2000
	time_interval_change_ms: float = 25

	ready_to_render: bool = False
	# todo: fix
	last_connection_time: float = time.perf_counter()


	def __init__(self, stdscr):
		self.stdscr = stdscr

		# visibility can be set to 0, 1, or 2, for invisible, normal, or very visible
		curses.curs_set(0)

		# Initialize colors
		curses.start_color()
		curses.use_default_colors()

		instructional_text = 1; curses.init_pair(instructional_text, curses.COLOR_BLUE, curses.COLOR_BLACK)


		self.top_bar_win = curses.newwin(5, 80, 0, 0)
		self.bottom_win = curses.newwin(15, 80, 5, 0)
		self.error_win = curses.newwin(5, 80, 20, 0)
		self.stdscr.refresh()

		self.top_bar_win.addstr(0, 0, "Welcome to the direct control", curses.color_pair(instructional_text))
		self.top_bar_win.addstr(1, 0, "Press ! to generate or regenerate the commands", curses.color_pair(instructional_text))
		self.top_bar_win.addstr(2, 0, "Press Esc to exit the program", curses.color_pair(instructional_text))
		self.top_bar_win.refresh()


	def generate_command_screen(self):
		self.bottom_win.clear()
		self.command_x_pos.clear()
		self.command_y_pos.clear()

		#30 commands maximum, each name 35 chars at most 15 line
		count = 0
		for command_name in self.command_pins.keys():
			if count < 30:
				self.command_y_pos[command_name] = count % 15

				self.command_x_pos[command_name] = 40 * int(count / 15)

			count += 1

		#generate block of command names
		for name in self.command_pins.keys():
			self.bottom_win.addstr(self.command_y_pos[name], self.command_x_pos[name], name)

		self.bottom_win.refresh()

		self.error_win.clear()
		self.error_win.refresh()

		self.ready_to_render = True;


	def render_time_interval_change(self, time_interval_change):

		if self.time_interval_ms + time_interval_change > self.max_time_interval_ms:
			self.time_interval_ms = self.max_time_interval_ms
		elif self.time_interval_ms + time_interval_change < self.min_time_interval_ms:
			self.time_interval_ms = self.min_time_interval_ms
		else:

			self.time_interval_ms += time_interval_change

		self.top_bar_win.addstr(1, 0, f"time interval ms: {self.time_interval_ms}  ")

		self.top_bar_win.refresh()

	#The return indicates success
	def generate_dictionaries_from_json(self):
		import json
		import re

		hardware_info = JetsonNanoPins()


		# Define the file name or path
		file_name = "command_key_groups.json"

		#open command file to extract data
		try:
			# Open the file in read mode
			with open(file_name, "r") as f:
				# Load the JSON data from the file
				data = json.load(f)
		except FileNotFoundError as e:
			# Handle the FileNotFoundError
			file_not_found_error = f"File {file_name} does not exist or is invalid: "
			self.__render_error_message(file_not_found_error + str(e))
			return False
		except PermissionError as e:
			# Handle the PermissionError
			file_needs_read_permission_error = f"File {file_name} cannot be opened and read due to insufficient permissions: "
			self.__render_error_message(file_needs_read_permission_error + str(e))
			return False
		except ValueError as e:
			# Handle the ValueError or JSONDecodeError
			bad_json_format_error = f"File {file_name} is not a valid JSON format or contains extra data: "
			self.__render_error_message(bad_json_format_error + str(e))
			return False

		#error handling
		max_num_commands = 30

		allowed_name_chars_pattern = re.compile("^[0-9a-zA-Z-_ ]+$")
		max_name_len = 35

		allowed_keys_pattern = re.compile("^[a-zA-Z]+$")

		#check the number of commands in the command_key_groups.json
		current_num_of_commands = len(data)
		if current_num_of_commands > max_num_commands:
			too_many_commands_error = f"{current_num_of_commands} commands is too many, only a max of {max_num_commands} allowed "
			__render_error_message(too_many_commands_error)
			return False


		command_pins_local_dict = {}
		command_keys_local_dict = {}


		# to check for duplicates of the same key or name
		non_duplicate_names = set()
		non_duplicate_keys = set()

		for entry in data:
			command_name = entry["name"]
			command_key = entry["key"]
			command_pin_list = entry["pins"]

			#check that name is a string
			if not isinstance(command_name, str):
				name_is_not_str_error = f"command \"{command_name}\" is of the worng type, only string is allowed for the name field"
				self.__render_error_message(name_is_not_str_error)
				return False

			#check that the name is not a duplicate
			if command_name in non_duplicate_names:
				duplicate_name_error = f"the command \"{command_name}\" apears more than once in the {file_name}"
				self.__render_error_message(duplicate_name_error)
				return False

			#check that key is also a string
			if not isinstance(command_key, str):
				key_is_not_str_error = f"key field for command \"{command_name}\" must be a string"
				self.__render_error_message(key_is_not_str_error)

			#check that the key is not a duplicate
			if command_key in non_duplicate_keys:
				first_instance_name = command_keys_local_dict[command_key]
				duplicate_key_error = f"key field \"{command_key}\" for command \"{command_name}\" apears twice, the first command with this key is named \"{first_instance_name}\""
				self.__render_error_message(duplicate_key_error)

			#check the name against the allowed chars
			if not allowed_name_chars_pattern.match(command_name):
				char_not_allowed_in_name_error = f"the name \"{command_name}\" is not allowed, only letters, numbers, underscores, dashes, and spaces allowed"
				self.__render_error_message(char_not_allowed_in_name_error)
				return False

			#check that the command name is not too long
			if len(command_name) > max_name_len:
				name_is_to_long_error = f"the name \"{command_name}\" of length {len(command_name)} is to long, only {max_name_len} chars allowed for the name"
				self.__render_error_message(name_is_to_long_error)
				return False

			#check that there is one and only one key
			if len(command_key) != 1:
				one_key_error = f"the key field for command \"{command_name}\" can have one and only one key"
				self.__render_error_message(one_key_error)
				return False

			#check the key against the allowed chars/keyboard inputs
			if not allowed_keys_pattern.match(command_key):
				keyboard_input_not_allowed_error = f"key field for command \"{command_name}\" is not allowed, only upper and lower case letter key inputs inputs allowed"
				self.__render_error_message(keyboard_input_not_allowed_error)
				return False

			#check that pins are a list of ints and/or floats
			if not isinstance(command_pin_list, list):
				command_pins_not_a_list_error = f"the pins field for \"{command_name}\" must be a list"
				self.__render_error_message(command_pins_not_a_list_error)
				return False
			else:
				non_duplicate_pins = set()
				for pin in command_pin_list:

					#check that each called pin is a valid pin on the hardware
					if not hardware_info.is_valid_pin(pin):
						command_pins_not_valid = f"the pins field for \"{command_name}\" must adhere to the GPIO standards"
						self.__render_error_message(command_pins_not_valid)
						return False

					#check that there are not duplicate pins
					if pin in non_duplicate_pins:
						duplicate_pin_error: str = f"the pins field for command \"{command_name}\" has duplicates"
						self.__render_error_message(duplicate_pin_error)
						return False

					non_duplicate_pins.add(pin)

			
			
			#for duplicate checking
			non_duplicate_names.add(command_name)
			non_duplicate_keys.add(command_key)

			#fill in dictionaries of commands
			command_pins_local_dict[command_name] = command_pin_list
			command_keys_local_dict[command_key] = command_name
			
			

		
		# do the assignments at the end
		self.command_pins.clear()
		self.command_pins = command_pins_local_dict
		self.command_keys.clear()
		self.command_keys = command_keys_local_dict

		#clear in case old commands get deleted or replaced
		self.command_in_use.clear()

		#since no errors and sucessful generation
		self.error_win.clear()
		self.top_bar_win.clear()
		
		return True

	def __render_error_message(self, error_message):

		self.error_win.clear()

		error_text: int = 4; curses.init_pair(error_text, curses.COLOR_RED, curses.COLOR_BLACK)


		[start_y, start_x] = [0,0]


		self.error_win.addstr(start_y, start_x, "Error: ", curses.color_pair(error_text))
		for line_y_pos in range(start_y + 1, 5):
			line = str()
			if len(error_message) >= self.max_screen_width:
				line = error_message[:self.max_screen_width]
				error_message = error_message[self.max_screen_width:]
			elif len(error_message) > 1:
				line = error_message
				error_message = str()
			else:
				pass

			self.error_win.addstr(line_y_pos, start_x, line, curses.color_pair(error_text))

		self.error_win.refresh()

	def handle_key_hit(self, command_key_str) -> bool:

		#check if key is valid
		if command_key_str not in self.command_keys.keys():
			return False

		command_name = self.command_keys[command_key_str]

		#TODO: maybe see if time is close to time interval to save ros network calls
		self.command_in_use[command_name] = time.perf_counter()

		text_in_use = 3; curses.init_pair(text_in_use, curses.COLOR_GREEN, curses.COLOR_BLACK)
		self.bottom_win.addstr(self.command_y_pos[command_name], self.command_x_pos[command_name], command_name, curses.color_pair(text_in_use))
		self.bottom_win.refresh()


		return True

	def DEBUG(self):
		debug_text = 5; curses.init_pair(debug_text, curses.COLOR_WHITE, curses.COLOR_GREEN)
		self.bottom_win.addstr(5,5, "got here",  curses.color_pair(debug_text))
		self.bottom_win.refresh()
		while True:
			curses.init_pair(debug_text, curses.COLOR_WHITE, curses.COLOR_GREEN)
			self.bottom_win.refresh()
			time.sleep(0.25)
			curses.init_pair(debug_text, curses.COLOR_WHITE, curses.COLOR_RED)
			self.bottom_win.refresh()
			time.sleep(0.25)