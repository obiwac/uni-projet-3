PATH = "~/user_data/shopping_list"

class List:
	__STATE_NORMAL = 0
	__STATE_REM_CONFIRM = 1
	__STATE_CLEAR_CONFIRM = 2

	def __init__(self, rhasspy):
		self.__state = List.__STATE_NORMAL
		self.__rhasspy = rhasspy

		try:
			self.read()

		except FileNotFoundError:
			# dictionnary where the keys are the object name, and the values are their count
			self.__elements = {}

	def __str__(self):
		s = ""

		for name in self.__elements:
			count = self.__elements[name]
			s += f"{count} {name}\n"

		return s

	def add(self, name, count):
		if name not in self.__elements:
			self.__elements[name] = 0

		if len(self.__elements) > 50:
			self.__rhasspy.text_to_speech("Vous avez dépassé le nombre d'éléments autorisées sur votre liste des courses pour la version de base de votre abonnement ! Veuillez payer pour l'abonnement premium...")

		self.__elements[name] += count
		self.write() # save after adding each element, just in case

		self.__rhasspy.text_to_speech(f"{count} {name} ajoutés à la liste des courses")

	def rem(self, name):
		if name not in self.__elements:
			return

		count = self.__elements[name]

		del self.__elements[name]
		self.write()

		self.__rhasspy.text_to_speech(f"{count} {name} supprimés de la liste des courses")

	def speak(self):
		for name in self.__elements:
			count = self.__elements[name]
			self.__rhasspy.text_to_speech(f"{count} {name}")

	def clear(self):
		self.count = len(self.__elements)

		self.__elements = {}
		self.write()

		self.__rhasspy.text_to_speech(f"{count} éléments supprimés de la liste des courses")

	def __process_normal(self, action, params):
		if action == "List_add":
			self.add(params["item"], params["count"])

		elif action == "List_rem":
			self.__state = List.__STATE_REM_CONFIRM
			self.__params = params.copy()

		elif action == "List_clear":
			self.clear()

		elif action == "List_speak":
			self.speak()

	def __process_rem_confirm(self, action, params):
		if action == "Confirm":
			self.rem(params["item"])

		self.__state = List.__STATE_NORMAL

	def __process_clear_confirm(self, action, params):
		if action == "Confirm":
			self.clear()

		self.__state = List.__STATE_NORMAL

	def process(self, action, params):
		funcs = (self.__process_normal, self.__process_rem_confirm, self.__process_clear_config)
		funcs[self.__state](action, params)

	def read(self):
		self.clear()

		with open(PATH, "r") as f:
			lines = f.readlines()

			for line in lines:
				name, count = line.split()
				self.__elements[name] = count

	def write(self):
		with open(PATH, "w") as f:
			f.write(str(self))
