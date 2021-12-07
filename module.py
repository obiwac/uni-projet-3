# a module is an individual part of the program (e.g. one module could be the shopping list, the other could be the flashlight)
# the Module class is what all modules inherit from, and provides basic functionality common to all modules

USER_DATA_PATH = "/home/pi/user_data/"

class Module:
	def __init__(self, rhasspy = None): # default value of None because not all modules require Rhasspy
		self.__rhasspy = rhasspy

	def __str__(self):
		return f"Generic module ({type(self)})"

	# sugar around rhasspy

	def say(self, msg):
		self.__rhasspy.text_to_speech(msg)

	def await_speech(self):
		intent = self.__rhasspy.speech_to_intent()
		return intent["name"], intent["params"]

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
