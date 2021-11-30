PATH = "~/user_data/shopping_list"

class List:
	def __init__(self):
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
			print("Vous avez dépassé le nombre d'éléments autorisées sur votre liste des courses pour la version de base de votre abonnement ! Veuillez payer pour l'abonnement premium...")

		self.__elements[name] += count
		self.write() # save after adding each element, just in case

	def rem(self, name):
		if name not in self.__elements:
			return

		del self.__elements[name]

	def clear(self):
		self.__elements = {}

	def process_command(self, action, params):
		if action == "Add":
			self.add(params["item"], params["count"])
			return True

		elif action == "Remove":
			self.rem(params["item"])
			return True

		elif action == "Clear":
			self.clear()
			return True

		return False

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
