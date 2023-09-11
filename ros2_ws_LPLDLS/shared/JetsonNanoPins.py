import time

class JetsonNanoPins:
	__pin_in_use = {}
	__pin_modification_times = {}

	__most_recent_modification_time = None

	__starting_valid_pin: int = 0
	__ending_valid_pin: int = 40
	def __init__(self):
		self.__starting_valid_pin: int = 0
		self.__ending_valid_pin: int = 40

		init_time = time.perf_counter()

		for pin_num in range(self.__starting_valid_pin, self.__ending_valid_pin + 1):
			self.__pin_in_use[pin_num] = False
			self.__pin_modification_times[pin_num] = init_time
		self.__most_recent_modification_time = init_time

	def get_pin_mod_time(self, pin):
		return self.__pin_modification_times[pin]

	def get_mod_time(self):
		return self.__most_recent_modification_time

	def get_pin_use(self, pin):
		return self.__pin_in_use[pin]

	#return indicates if change occured or not
	def set_pin_use(self, pin, new_value) -> bool:

		return_bool = new_value ^ self.__pin_in_use[pin]

		self.__pin_in_use[pin] = new_value

		modification_time = time.perf_counter()

		self.__pin_modification_times[pin] = modification_time

		self.__most_recent_modification_time = modification_time

		return return_bool

	def get_pins(self) -> set:
		return self.__pin_in_use.keys()


	def is_valid_pin(self, pin_num) -> bool:

		if not (isinstance(pin_num, int) or isinstance(pin_num, float)):
			return False
		if int(pin_num) < self.__starting_valid_pin or int(pin_num) > self.__ending_valid_pin:
			return False

		return True