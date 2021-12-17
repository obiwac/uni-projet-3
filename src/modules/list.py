import graphics
import module

class List(module.Module):
	def __init__(self):
		"""
		Read the current shopping list if it already exists.
		If not, set the elements dictionnary to 'None' for now.
		"""

		super().__init__()

		# dictionnary where the keys are the object item, and the values are their count
		self.__elements = {}

		try:
			self.read()

		except FileNotFoundError:
			pass

	def __str__(self):
		"""
		Format the shopping list correctly, with each element's item name followed by its count.
		"""

		s = ""

		for item in self.__elements:
			count = self.__elements[item]
			s += f"{item} {count}\n"

		return s

	def add(self, params):
		"""
		Add 'item' to the shopping list 'count' times.
		If the key already exists in the elements dictionnary, add 'count'.
		Otherwise, create the key and set it to 'count'.
		Finally, write the shopping list to user data.
		"""

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
		"""
		Ask user for confirmation, then remove the 'item' key from the elements dictionnary.
		Show cool little animation, and then write the shopping list to user data.
		"""

		item = params["item"]

		if item not in self.__elements:
			graphics.animation("error")
			self.say(f"Vous n'avez pas de {item} dans votre liste des courses")
			return

		count = self.__elements[item]

		if not self.confirm(f"Êtes-vous sûr de vouloir supprimer {count} {item} de la liste des courses?"):
			return

		graphics.image(f"items/{item}")
		self.say(f"Suppression de {count} {item}")
		graphics.image(f"items/{item}", crossed = True)

		del self.__elements[item]
		self.write()

	def speak(self, params):
		"""
		Read out load the shopping list.
		If there are yet no elements in it, give an error message.
		Show images for each element spoken.
		"""

		if not self.__elements:
			graphics.animation("error")
			self.say("Vous n'avez aucun élément dans votre liste des courses")

		for item in self.__elements:
			count = self.__elements[item]

			graphics.image(f"items/{item}")
			self.say(f"{count} {item}")

	def __clear(self):
		"""
		Clear the shopping list and write it to user data.
		"""

		self.__elements = {}
		self.write()

	def clear(self, params):
		"""
		Wrapper around '__clear' which asks for confirmation to the user first.
		"""

		count = len(self.__elements)

		if not self.confirm(f"Êtes-vous sûr de vouloir supprimer {count} éléments de la liste des courses?"):
			return

		self.__clear()

		graphics.animation("success")
		self.say(f"{count} éléments supprimés de la liste des courses")

	def process(self, action, params):
		"""
		Process potential shopping list commands.
		"""

		exported = {
			"List_add": self.add,
			"List_rem": self.rem,
			"List_clear": self.clear,
			"List_speak": self.speak,
		}

		if action in exported:
			exported[action](params)

	def read(self):
		"""
		Read and parse the shopping list from the shopping list file.
		"""

		lines = self.read_user_data("shopping_list")

		for line in lines:
			item, count = line.split()
			self.__elements[item] = int(count)

	def write(self):
		"""
		Write the shopping list to the shopping list file.
		"""
		
		self.write_user_data("shopping_list", str(self))
