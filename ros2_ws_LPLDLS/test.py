import threading
import time 

def waste_cpu_time():
	x = time.perfcounter()
	while True:
		dom = time.perfcounter() % 23
		x = x / dom


# import json
# from shared.JetsonNanoPins import JetsonNanoPins
# def my_func(passed_in_str) -> bool:
# 	print(passed_in_str)
# 	return bool(passed_in_str)


# print(my_func("To pass"))
# # tracker = JetsonNanoPins()

# my_str = json.dumps(tracker)
# # print(my_str)
# import json

# def open_and_read():
# 	#open command file
# 	#extract data
# 	try:
# 		with open("test_writes.json", "r") as f:
# 			# Load the JSON data from the file
# 			data = json.load(f)

# 	except:
# 		import os
# 		print("could not open and load, current working directory: " + os.getcwd())

# 	for entry in data:
# 		name: str = entry["field1"]
# 		numbers: list = entry["field2"]
# 		truth: bool = entry["field3"]
# 		print(f"FIELD_1: {name}, FIELD_2: {numbers}, FIELD_3: {truth}")

# 	return data



# def open_and_save(data):
# 	with open("test_writes.json", "w") as outfile:
# 		# Serialize and write the data
# 		json.dump(data, outfile, indent=4)


# temp_data = open_and_read()

# print("editing the data")

# for item in temp_data:
# 	item["field3"] = not item["field3"]

# open_and_save(temp_data)

# open_and_read()

"""
# from direct_control_shore.dep import *

# from direct_control_shore.dep import my_func
# var = 25
# my_func()
# from direct_control_shore.dep import my_class

# my_func()
# g = my_class()

# print(global_var)


# var: list(int) = [27,45,67]
# print(f"My var is {var}")
# my_dict = {"g", 25}
# if my_dict:
# 	print("True!!!")

# import time

# class Myclass:
# 	var: int = 0
# 	def get(self):
# 		return self.var
# 	def set(self, new_value):
# 		self.var = new_value

# obj = Myclass()
# print(str(obj.get()))
# my_num = obj.get()
# my_num += 5
# print(str(obj.get()))
# print(obj.var)




s = "temperature : [25.3, 26.7, 24.9, 27.1]"
parts = s.split(":")
type_action = parts[0].strip() # Use strip () to remove any leading or trailing whitespace
values = parts[1].strip()
values = values[1:-1]
print(type_action)
print(len(values))


import json
lst = [1, 2, 3, 4, 5] # original list
s = json.dumps(lst) # convert list to JSON string
my_str: str = s

lst = json.loads("[1, 2, 3, 4, 5]") # parse JSON string back to list

for val in lst:
	print(val)

# import json
# values = json.loads("[1, 2, 3.1]")
# for val in values:
# 	if isinstance(val, int):
# 		print("integer!")
# 	elif isinstance(val, float):
# 		print("float!")
# 	else:
# 		print("wrong!")

# import json
# my_set = set([json.loads("[1, 2, 3.1]")])
# for val in my_set:
# 	if isinstance(val, int):
# 		print("integer!")
# 	elif isinstance(val, float):
# 		print("float!")
# 	else:
# 		print("wrong!")


# print(str(min(abs(-2), 0)))
"""


# class my_class:
# 	def outer(self):
# 		return

# 	def private_name(self):
# 		print("Goit here")
# 		return
# 	def public(self):
# 		self.private_name()
# 		return

# import json	

# # obj = my_class()
# # obj.private_name()

# #open command file
# #extract data
# try:
# 	with open("test_writes.json", "r") as f:
# 		# Load the JSON data from the file
# 		data = json.load(f)

# except:
# 	import os
# 	print("could not open and load, current working directory: " + os.getcwd())

# num = len(data)
# print(f"num = {num}")


#######################################################################################################################
"""

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
	max_screen_height: int = 20
	command_x_pos = {}
	command_y_pos = {}


	time_interval_ms: float = 500
	min_time_interval_ms: float = 25
	max_time_interval_ms: float = 2000
	time_interval_change_ms: float = 25

	stdscr = None

	def __init__(self):
		pass

	def __init__(self, stdscr):
		pass
		# self.stdscr = stdscr

		# # Initialize colors
		# curses.start_color()
		# curses.use_default_colors()

		# instructional_text = 1; curses.init_pair(instructional_text, curses.COLOR_BLUE, curses.COLOR_BLACK)

		# stdscr.addstr(0, 0, "Welcome to the direct control", curses.color_pair(instructional_text))
		# stdscr.addstr(1, 0, "Press ! to generate or regenerate the commands", curses.color_pair(instructional_text))
		# stdscr.addstr(2, 0, "Press Esc to exit the program", curses.color_pair(instructional_text))
		# stdscr.refresh()

	
	# def generate_command_screen(self):
	# 	self.stdscr.clear()
	# 	self.command_x_pos.clear()
	# 	self.command_y_pos.clear()

	# 	vertical_offset = 1
	# 	total_space_per_name = 30

	# 	vertical_count = 0
	# 	horizontal_count = 0
	# 	for name in self.command_pins.keys():
	# 		if (vertical_count + vertical_offset > 10): #max_screen_height
	# 			horizontal_count += total_space_per_name
	# 			vertical_count = 0
	# 		self.command_x_pos[name] = horizontal_count
	# 		self.command_y_pos[name] = vertical_count + vertical_offset
	# 		if (vertical_count + vertical_offset <= 10):
	# 			vertical_count += 1


	# 	#generate block of command names
	# 	for name in self.command_pins.keys():
	# 		self.stdscr.addstr(self.command_y_pos[name], self.command_x_pos[name], name)

	# 	self.stdscr.refresh()

	# def render_time_interval_change(self, time_interval_change):
	# 	# self.debug()
	# 	if self.time_interval_ms + time_interval_change > self.max_time_interval_ms:
	# 		self.time_interval_ms = self.max_time_interval_ms
	# 	elif self.time_interval_ms + time_interval_change < self.min_time_interval_ms:
	# 		self.time_interval_ms = self.min_time_interval_ms
	# 	else:

	# 		self.time_interval_ms += time_interval_change

	# 	self.stdscr.addstr(0, 20, f"time interval ms: {self.time_interval_ms}  ")

	# 	self.stdscr.refresh()
	
import curses
import time
# from curses.textpad import Textbox, rectangle

def main(stdscr):
	stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

	editwin = curses.newwin(5,30, 2,1)
	# rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
	stdscr.refresh()

	
	box = Textbox(editwin)

	# Let the user edit until Ctrl-G is struck.
	box.edit()

	# Get resulting contents
	message = box.gather()
	

	editwin.addstr(0,0, "got here!")
	editwin.refresh()


	ortd()
	# my_win = curses.newwin(1,30, 10, 1)
	# my_win.addstr(0,0,message)
	# my_win.refresh()

	# stdscr.refresh()

	time.sleep(2.0)


# curses.wrapper(main)

# maping = {"her": 6, "hg" : 67, "hgf" : 78}

# my_set = maping.keys()

# key = ord("j")

# print(str(chr(key)) in my_set)

# try:
# 	# Run the program
# 	curses.wrapper(main)
# 	# rclpy.spin(minimal_publisher)
# except Exception as e:
# 	# Handle any exception that may occur
# 	# Print the error message
# 	print(f"An error occurred: {e}")

def thread_function(text_set):
	try:
		other_function()
	except Exception as e:
		print("inside!")
		text_set.add(str(e))
		return text_set

def other_function():
	non_existant_function()

# import threading

# text_set = set()

# t_test = threading.Thread(target = thread_function, args = [text_set], daemon = True)
# t_test.start()

# t_test.join()

# print(text_set)
def reverse_slice(text, start, end):
    # Your code here
    return (text[start : end + 1])[::-1]

rs = reverse_slice("This should give me the answer",3,11)
if rs is None:
  print("Function didn't return anything")
else:
  print(hash(rs))

# get the hash for correct answer and set up the quiz
"""