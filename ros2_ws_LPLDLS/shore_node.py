

# for command generation from file
import json
import re

import threading
import time

in_contact_with_nano_lock = threading.Lock()
in_contact_with_nano = False

user_interface_lock = threading.Lock()


command_pins = {}
command_keys = {}
command_in_use = {}




def generate_commands():

    #open command file
    #extract data
    try:
        with open("commands.json", "r") as f:
            # Load the JSON data from the file
            data = json.load(f)
    except:
        import os
        error_message = "could not open or load commands, current working directory: " + os.getcwd()

        return [False, error_message]
    
    command_pins.clear()
    command_keys.clear()
    command_in_use.clear()

    #error handling
    max_num_commands = 30
    counted_commands = 0

    starting_valid_pin = 0
    ending_valid_pin = 40

    name_pattern = re.compile("^[0-9a-zA-Z-_ ]+$")
    max_name_chars = 30

    key_pattern = re.compile("^[a-zA-Z]+$")


    for command in data:
        #check the number of commands
        counted_commands += 1
        if counted_commands > max_num_commands:
            error_message = (f"to many commands, only {max_num_commands} commands allowed")
            return [False, error_message]
        #check the name
        if not name_pattern.match(command["name"]):
            error_message = (command["name"] + " is a bad name, only letters, numbers, underscores, dashes, and spaces allowed")
            return [False, error_message]
        if len(command["name"]) > max_name_chars:
            error_message = (command["name"] + f" is a bad name, only {max_name_chars} chars allowed for each name")
            return [False, error_message]
        #check the key binding
        if not key_pattern.match(command["key"]):
            error_message = (command["key"] + " for "  + command["name"] + "is a bad key binding, only letters allowed")
            return [False, error_message]
        if len(command["key"]) != 1:
            error_message = (command["key"] + " for "  + command["name"] + "is a bad key binding, only one key allowed")
            return [False, error_message]
        #check valid pins
        for pin in command["pins"]:
            if (pin <= starting_valid_pin) or (pin >= ending_valid_pin):
                error_message = (f"bad pin, only pins between {starting_valid_pin} and {ending_valid_pin} are allowed")
                return [False, error_message]

        #fill in dictionaries of commands
        command_pins[command["name"]] = command["pins"]
        command_keys[command["key"]] = command["name"]

    return [True, ""]

def generate_error_message(error_message, stdscr):
    error_text = 2; curses.init_pair(error_text, curses.COLOR_RED, curses.COLOR_BLACK)

    message_width = max_screen_width
    stdscr.addstr(5, 0, "Error: ", curses.color_pair(error_text))
    for line in range(6, max_screen_height):
        for i in range(0,message_width):
            stdscr.addstr(line, i, " ")
        if len(error_message) >= message_width:
            stdscr.addstr(line, 0, error_message[:message_width], curses.color_pair(error_text))
            error_message = error_message[message_width:]
        elif len(error_message) > 0:
            stdscr.addstr(line, 0, error_message, curses.color_pair(error_text))
            error_message = ""
        else:
            pass

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





def handle_time_change(stdscr, time_change_ms):
    global min_time_interval_ms
    global max_time_interval_ms
    global time_interval_ms

    if time_interval_ms + time_change_ms < min_time_interval_ms:
        time_interval_ms = min_time_interval_ms
    elif time_interval_ms + time_change_ms > max_time_interval_ms:
        time_interval_ms = max_time_interval_ms
    else:
        time_interval_ms += time_change_ms

    #TODO:
    #ROS2 Stuff here

    user_interface_lock.acquire()
    stdscr.addstr(0, 40, f"time interval: {time_interval_ms} ms ")
    stdscr.refresh()
    user_interface_lock.release()
    return time_interval_ms

def handle_key_usage_removal(stdscr):
    global command_in_use
    global time_interval_ms
    while True:
        user_interface_lock.acquire()
        if command_in_use:

            #access the min IE oldest entry
            oldest_command_name = min(command_in_use.keys(), key=lambda k: command_in_use[k])

            
            #Check that it is past due and expell it
            if ((time.perf_counter() - command_in_use[oldest_command_name]) * 1000) >= time_interval_ms:

                command_in_use.pop(oldest_command_name)

                #update the UI
                stdscr.addstr(command_y_pos[oldest_command_name], command_x_pos[oldest_command_name], oldest_command_name)
                stdscr.refresh()
                user_interface_lock.release()
            #Wait for it to expire
            else:
                sleep_time = 50 / 1000
                user_interface_lock.release()
                time.sleep(sleep_time)
        else:

            user_interface_lock.release()

            time.sleep(50 / 1000)
        


import curses

max_screen_width = 80
max_screen_height = 20
command_x_pos = {}
command_y_pos = {}

time_interval_ms = 500
min_time_interval_ms = 25
max_time_interval_ms = 2000


# # Initialize curses
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)
def direct_control(stdscr):
    #ROS2
    rclpy.init(args=None)
    Publisher = DirectControlPublisher()



    # Initialize colors
    curses.start_color()
    curses.use_default_colors()

    instructional_text = 1; curses.init_pair(instructional_text, curses.COLOR_BLUE, curses.COLOR_BLACK)


    stdscr.addstr(0, 0, "Welcome to the direct control", curses.color_pair(instructional_text))
    stdscr.addstr(1, 0, "Press ! to generate or regenerate the commands", curses.color_pair(instructional_text))
    stdscr.addstr(2, 0, "Press Esc to exit the program", curses.color_pair(instructional_text))

    
    threading.Thread(target=handle_key_usage_removal, args = [stdscr] , daemon = True).start()

    while True:
        # Get a key
        key = stdscr.getch()


        # for processing the commands from the file
        if key == ord("!"):
            user_interface_lock.acquire()
            [success, error_message] = generate_commands()
            if success:
                generate_command_screen(stdscr)
            else:
                generate_error_message(error_message, stdscr)       
            stdscr.refresh()
            user_interface_lock.release()

        # for changing the time interval at runtime
        if key == ord("+") or key == ord("="):
            new_time_interval_ms = handle_time_change(stdscr, 25)

            #TODO:
            #ROS2 stuff here
            ROS2_msg = f"Increasing time interval to {new_time_interval_ms}"
            Publisher.single_call(ROS2_msg)


        if key == ord("-") or key == ord("_"):
            new_time_interval_ms = handle_time_change(stdscr, -25)

            #TODO:
            #ROS2 stuff here
            ROS2_msg = f"Decresing time interval to {new_time_interval_ms}"
            Publisher.single_call(ROS2_msg)           

        if str(chr(key)) in command_keys:


            command_name = command_keys[str(chr(key))]
            user_interface_lock.acquire()

            if command_name in command_in_use.keys():

                holding_down_key_interval_ms = 10 
                if (time.perf_counter() - command_in_use[command_name] * 1000) <= holding_down_key_interval_ms:
                    command_in_use[command_name] = time.perf_counter()
                    #let the update deamon handle it

                    #TODO:
                    #ROS2 stuff here
                    PINS = command_pins[command_name]
                    ROS2_msg = "NAME: " + command_name + f", PINS: {PINS}"
                    Publisher.single_call(ROS2_msg)

                else:
                    pass
            else:
                command_in_use[command_name] = time.perf_counter()

                #TODO:
                #ROS2 stuff here
                PINS = command_pins[command_name]
                ROS2_msg = "NAME: " + command_name + f", PINS: {PINS}"
                Publisher.single_call(ROS2_msg)

                in_use_color = 3; curses.init_pair(in_use_color, curses.COLOR_GREEN, curses.COLOR_BLACK)
                stdscr.addstr(command_y_pos[command_name], command_x_pos[command_name], command_name, curses.color_pair(in_use_color))
                stdscr.refresh()
                #update the UI


            user_interface_lock.release()

        # Exit if ESC is pressed
        if key == 27:
            #for ROS2
            rclpy.shutdown()
            # Destroy the node explicitly
            # (optional - otherwise it will be done automatically
            # when the garbage collector destroys the node object)
            Publisher.destroy_node()
            rclpy.shutdown()

            # Restore terminal settings
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            break



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

if __name__ == '__main__':

    pass
    # Run the program
    # curses.wrapper(main)
    # rclpy.spin(minimal_publisher)


def main(args = None):

    #run program
    curses.wrapper(direct_control)
    # rclpy.spin(minimal_publisher)

curses.wrapper(direct_control)
# if __name__ == '__main__':
#     print("inside the wierd if statment")
#     #main()


