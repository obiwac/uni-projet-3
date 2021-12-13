import graphics
import module

class List(module.Module):
	def __init__(self):
		super().__init__()

		try:
			self.read()

		except FileNotFoundError:
			# dictionnary where the keys are the object item, and the values are their count
			self.__elements = {}

	def __str__(self):
		s = ""

		for item in self.__elements:
			count = self.__elements[item]
			s += f"{item} {count}\n"

		return s

	def add(self, params):
		item = params["item"]
		count = params["count"]

		if item not in self.__elements:
			self.__elements[item] = 0

		if len(self.__elements) > 4:
			self.say("Vous avez dépassé le nombre d'éléments autorisées sur votre liste des courses pour la version de base de votre abonnement ! Veuillez payer pour l'abonnement premium...")

		graphics.image(f"items/{item}")

		self.__elements[item] += count
		self.write() # save after adding each element, just in case

		self.say(f"{count} {item} ajoutés à la liste des courses")

	def rem(self, params):
		item = params["item"]

		if item not in self.__elements:
			graphics.error()
			self.say(f"Vous n'avez pas de {item} dans votre liste des courses")
			return

		count = self.__elements[item]

		if not self.confirm(f"Êtes-vous sûr de vouloir supprimer {count} {item} de la liste des courses?"):
			return

		graphics.image(f"items/{item}", crossed = True)

		del self.__elements[item]
		self.write()

		self.say(f"{count} {item} supprimés de la liste des courses")

	def speak(self, params):
		if not self.__elements:
			graphics.error()
			self.say("Vous n'avez aucun élément dans votre liste des courses")

		for item in self.__elements:
			count = self.__elements[item]

			graphics.image(f"items/{item}")
			self.say(f"{count} {item}")

	def __clear(self):
		self.__elements = {}
		self.write()

	def clear(self, params):
		count = len(self.__elements)

		if not self.confirm(f"Êtes-vous sûr de vouloir supprimer {count} éléments de la liste des courses?"):
			return

		self.__clear()

		graphics.success()
		self.say(f"{count} éléments supprimés de la liste des courses")

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
		lines = self.read_user_data("shopping_list")
		self.__clear()

		for line in lines:
			item, count = line.split()
			self.__elements[item] = count

	def write(self):
		self.write_user_data("shopping_list", str(self))
