# a module is an individual part of the program (e.g. one module could be the shopping list, the other could be the flashlight)
# the Module class is what all modules inherit from, and provides basic functionality common to all modules

import math

USER_DATA_PATH = "/home/pi/user_data/"

X_RES = 8
Y_RES = 8

class Module:
	rhasspy = None
	sense = None

	# drawing attributes

	fb = [[(0, 0, 0)] * X_RES] * Y_RES
	theta = 0

	def __init__(self):
		pass

	def __str__(self):
		return f"Generic module ({type(self)})"

	# sugar around rhasspy

	def say(self, msg):
		self.rhasspy.text_to_speech(msg)

	def await_speech(self):
		intent = self.rhasspy.speech_to_intent()
		return intent["name"], intent["variables"]

	# drawing code

	@classmethod
	def rotate_point(self, rotated_fb, c, s, x, y, colour):
		x -= X_RES // 2
		y -= Y_RES // 2

		x = x * c - y * s
		y = x * s + y * c

		try:
			rotated_fb[int(x)][int(y)] = colour

		except IndexError:
			pass

	@classmethod
	def flip(self):
		rotated_fb = [[(0, 0, 0)] * X_RES] * Y_RES

		s = math.sin(self.theta)
		c = math.cos(self.theta)

		for y in range(Y_RES):
			for x in range(X_RES):
				rotate_point(rotated_fb, c, s, x, y, self.fb[x][y])
				colour = self.fb[x][y]

		self.sense.set_pixels(rotated_fb)

	@classmethod
	def render(self):
		self.flip()

	@classmethod
	def wash(self, r, g, b):
		self.fb = [[(r, g, b)] * X_RES] * Y_RES

	# utility functions

	def confirm(self, msg = "Veuillez confirmer l'action"):
		self.say(msg)

		while True:
			action, _ = self.await_speech()

			if action == "Confirm":
				return True

			if action == "Cancel":
				self.say("Annulation de l'opération")
				return False

	def read_user_data(self, file):
		with open(f"{USER_DATA_PATH}{file}", "r") as f:
			return f.readlines()

	def write_user_data(self, file, data):
		# open with 'w+' mode to create file if it doesn't already exist

		with open(f"{USER_DATA_PATH}{file}", "w+") as f:
			f.write(data)
