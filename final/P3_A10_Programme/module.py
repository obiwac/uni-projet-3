# a module is an individual part of the program (e.g. one module could be the shopping list, the other could be the flashlight)
# the Module class is what all modules inherit from, and provides basic functionality common to all modules

import graphics

USER_DATA_PATH = "/home/pi/user_data/"

X_RES = 8
Y_RES = 8

class Module:
	rhasspy = None

	def __init__(self):
		pass

	def __str__(self):
		return f"Generic module ({type(self)})"

	# sugar around rhasspy

	def say(self, msg):
		"""
		Wrapper around Rhasspy's 'text_to_speech' function.
		"""

		print(f"Say: {msg}")
		self.rhasspy.text_to_speech(msg)

	def await_speech(self):
		"""
		Show microphone animation and await for speech.
		Wrapper around Rhasspy's 'speech_to_intent' function.
		"""

		graphics.animation("mic")
		print("Awaiting speech ...")
		intent = self.rhasspy.speech_to_intent()
		return intent["name"], intent["variables"]

	# utility functions

	def confirm(self, msg = "Veuillez confirmer l'action"):
		"""
		Ask the user if they're sure they want to execute a certain action.
		'msg' is the prompt, and we return 'True' on confirmation or 'False' on cancellation.
		"""

		graphics.animation("question")
		self.say(msg)

		while True:
			action, _ = self.await_speech()

			if action == "Confirm":
				return True

			if action == "Cancel":
				graphics.animation("cancel")
				self.say("Annulation de l'opération")
				return False

	def read_user_data(self, file):
		"""
		Read a file from the user data directory.
		"""

		with open(f"{USER_DATA_PATH}{file}", "r") as f:
			return f.readlines()

	def write_user_data(self, file, data):
		"""
		Write a file to the user data directory.
		"""

		# open with 'w+' mode to create file if it doesn't already exist

		with open(f"{USER_DATA_PATH}{file}", "w+") as f:
			f.write(data)
