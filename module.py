# a module is an individual part of the program (e.g. one module could be the shopping list, the other could be the flashlight)
# the Module class is what all modules inherit from, and provides basic functionality common to all modules

class Module:
	def __init__(self, rhasspy):
		self.__rhasspy = rhasspy

	def __str__(self):
		return f"Generic module ({type(self)})"

	# sugar around rhasspy

	def say(self, msg):
		self.__rhasspy.text_to_speech(msg)

	def await_speech(self):
		return self.__rhasspy.speech_to_intent()

	# utility functions

	def confirm(self, msg = "Veuillez confirmer l'action"):
		self.say(msg)

		while True:
			intent = self.await_speech()
			action = intent["name"]

			if action == "Confirm":
				return True

			if action == "Cancel":
				self.say("Annulation de l'opération")
				return False
