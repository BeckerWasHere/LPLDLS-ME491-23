import argparse
import RPi.GPIO as GPIO
import time

state_A_pin_num1: int = 37
state_A_pin_num2: int = 38

state_B_pin_num1: int = 35
state_B_pin_num2: int = 36

enable_pin_num1:  int = 23 #was 31 # Was 29 # Was 31 # Was 33
enable_pin_num2:  int = 24

state_A = ["A", "a", "In1", "in1", "up", "UP"]
state_B = ["B", "b", "In2", "in2", "down", "DOWN"] # 15 seconds


# def custom_pwm_mode(time_seconds: float, pwm_out_100: int) -> None:
# 	# 1000 HZ duty cycle, 0.001 second chunks
# 	time_chunk: float = 0.001

# 	num_power_on_time_chunks = 1
# 	num_total_time_chunks = 1

# 	intital_time = time.perf_counter()
# 	while (time.perf_counter() - intital_time) < time_seconds:
# 		time.sleep(time_chunk)

# 		# if power on / total time < duty cycle
# 		if (num_power_on_time_chunks * 100) <= (pwm_out_100 * num_total_time_chunks):
# 			GPIO.output(enable_pin_num1, GPIO.HIGH)
# 			num_power_on_time_chunks += 1
# 		else:
# 			GPIO.output(enable_pin_num1, GPIO.LOW)

# 		num_total_time_chunks += 1
# 	print("ending pwm")


def main():

	# Create an ArgumentParser object
	parser = argparse.ArgumentParser(description="A simple Program to activate the H-bridge")

	parser.add_argument("-state", type=str, help="state on H-bridge to activate In1 or In2")

	parser.add_argument("-time", type=int, help="time in milliseconds to activate")

	# # Add an optional argument for the int with a default value of 0
	# parser.add_argument("-pwm", "-opt", type=int, default = 100, help="An optional number to print (default: 0)")

	# Parse the arguments
	args = parser.parse_args()

	if args.state not in state_A and args.state not in state_B:
		print("must indicate the state A or B")
		exit()

	if args.time is None:
		print("must supply -time [time in milliseconds]")
		exit()

	if int(args.time) < 1 or int(args.time) > 10000:
		print("-time TIME must be between 0 and 10000 milliseconds")
		exit()

	# if args.pwm < 1 or args.pwm > 100:
	# 	print("-pwm PWM must indicate a duty cycle between 1 and 100")
	# 	exit()
	

	GPIO.setmode(GPIO.BOARD)

	print("Activating the twos H-Bridges")

	# Both pairs of Inputs
	GPIO.setup(state_A_pin_num1, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(state_A_pin_num2, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(state_B_pin_num1, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(state_B_pin_num2, GPIO.OUT, initial=GPIO.LOW)

	# Enable Pair
	GPIO.setup(enable_pin_num1, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(enable_pin_num2, GPIO.OUT, initial=GPIO.LOW)
	GPIO.output(enable_pin_num1, GPIO.HIGH)
	GPIO.output(enable_pin_num2, GPIO.HIGH)


	working_time = args.time / 1000

	if args.state in state_A:
		GPIO.output(state_A_pin_num1, GPIO.HIGH)
		GPIO.output(state_A_pin_num2, GPIO.HIGH)

		time.sleep(working_time)

		GPIO.output(state_A_pin_num1, GPIO.LOW)
		GPIO.output(state_A_pin_num2, GPIO.LOW)

	elif args.state in state_B:
		GPIO.output(state_B_pin_num1, GPIO.HIGH)
		GPIO.output(state_B_pin_num2, GPIO.HIGH)

		time.sleep(working_time)

		GPIO.output(state_B_pin_num1, GPIO.LOW)
		GPIO.output(state_B_pin_num2, GPIO.LOW)
		
	else:
		pass

	GPIO.output(enable_pin_num1, GPIO.LOW)
	GPIO.output(enable_pin_num2, GPIO.LOW)
	

if __name__ == '__main__':
	try:
		main()
	finally:
		GPIO.output(state_A_pin_num1, GPIO.LOW)
		GPIO.output(state_A_pin_num2, GPIO.LOW)

		GPIO.output(state_B_pin_num1, GPIO.LOW)
		GPIO.output(state_B_pin_num2, GPIO.LOW)

		GPIO.output(enable_pin_num1, GPIO.LOW)
		GPIO.output(enable_pin_num2, GPIO.LOW)

		GPIO.cleanup()
		print("Program exit")