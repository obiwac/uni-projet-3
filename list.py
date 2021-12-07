import module

PATH = "~/user_data/shopping_list"

class List_module(Module):
	def __init__(self, rhasspy):
		super().__init__(rhasspy)

		try:
			self.read()

		except FileNotFoundError:
			# dictionnary where the keys are the object item, and the values are their count
			self.__elements = {}

	def __str__(self):
		s = ""

		for item in self.__elements:
			count = self.__elements[item]
			s += f"{count} {item}\n"

		return s

	def add(self, params):
		item = params["item"]
		count = params["count"]

		if item not in self.__elements:
			self.__elements[item] = 0

		if len(self.__elements) > 50:
			self.__rhasspy.text_to_speech("Vous avez dépassé le nombre d'éléments autorisées sur votre liste des courses pour la version de base de votre abonnement ! Veuillez payer pour l'abonnement premium...")

		self.__elements[item] += count
		self.write() # save after adding each element, just in case

		self.__rhasspy.text_to_speech(f"{count} {item} ajoutés à la liste des courses")

	def rem(self, params):
		item = params["item"]

		if item not in self.__elements:
			return

		count = self.__elements[item]

		if not self.confirm(f"Êtes-vous sûr de vouloir supprimer {count} {item} de la liste des courses?"):
			return

		del self.__elements[item]
		self.write()

		self.__rhasspy.text_to_speech(f"{count} {item} supprimés de la liste des courses")

	def speak(self, params):
		for item in self.__elements:
			count = self.__elements[item]
			self.__rhasspy.text_to_speech(f"{count} {item}")

	def __clear(self):
		self.__elements = {}
		self.write()

	def clear(self, params):
		self.count = len(self.__elements)

		if not self.confirm(f"Êtes-vous sûr de vouloir supprimer {count} éléments de la liste des courses?"):
			return

		self.__clear()

		self.__rhasspy.text_to_speech(f"{count} éléments supprimés de la liste des courses")

	def process(self, action, params):
		exported = {
			"List_add": self.add,
			"List_rem": self.rem,
			"List_clear": self.clear,
			"List_speak": self.speak,
		}

		if action in exported:
			exported[action](params)

	def read(self):
		self.__clear()

		with open(PATH, "r") as f:
			lines = f.readlines()

			for line in lines:
				item, count = line.split()
				self.__elements[item] = count

	def write(self):
		with open(PATH, "w") as f:
			f.write(str(self))
