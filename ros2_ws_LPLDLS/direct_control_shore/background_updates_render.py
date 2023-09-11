import time
import threading
def background_updates_render(screen_view, commands_model_lock):

	sleep_time_s: float = screen_view.min_time_interval_ms / 1000
	
	while True:
		commands_model_lock.acquire()

		#TODO test if it is worth it to pop from the command_last in use
		if screen_view.command_in_use:
			for name in screen_view.command_in_use.keys():
				#Check that it is past due and update
				if ((time.perf_counter() - screen_view.command_in_use[name]) * 1000) >= screen_view.time_interval_ms:
					#update UI
					screen_view.bottom_win.addstr(screen_view.command_y_pos[name], screen_view.command_x_pos[name], name)
			screen_view.bottom_win.refresh()

		commands_model_lock.release()
		
		#to not burn CPU time
		time.sleep(sleep_time_s)

