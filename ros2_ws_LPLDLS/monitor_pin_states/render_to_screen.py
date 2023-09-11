from shared.JetsonNanoPins import JetsonNanoPins
from monitor_pin_states.UserInterface import UserInterface

import time

import threading

#TODO: rename to just render

def handle_rendering_to_screen(shared_model, screen_view):
	sleep_time = 0.05 #TODO change this to be a better value

	while True:
		shared_model.lock.acquire()

		screen_view.render_main_content(shared_model.hardware_tracker)

		if 

		screen_view.render_status_bar(shared_model.b_recent_access)

		shared_model.lock.release()

		time.sleep(sleep_time)
	pass