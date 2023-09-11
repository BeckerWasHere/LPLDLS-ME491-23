from shared.JetsonNanoPins import JetsonNanoPins

import threading

class Model:
	hardware_tracker = None
	b_recent_access = None
	f_recent_access = None
	lock = threading.Lock()

	__init__(self, hardware_tracker):
		self.hardware_tracker = hardware_tracker
		b_recent_access = False
