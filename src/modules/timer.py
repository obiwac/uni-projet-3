import graphics
import module
from datetime import datetime

class Timer(module.Module):
	def __init__(self):
		super().__init__()
		self.__active = False

	def update(self):
		if not self.__active:
			return
		
		if (datetime.now() - self.__start).total_seconds() > self.__seconds:
			graphics.animation("success")
			self.say("Votre minuteur a expiré")

			self.__active = False

	def process(self, action, params):
		exported = {
			"Timer": self.timer,
		}

		if action in exported:
			exported[action](params)

	def timer(self, params):
		if self.__active:
			if not self.confirm(f"Un minuteur est déjà en place pour {self.__seconds} secondes. Voulez vous le remplacer?"):
				return

		self.__active = True

		self.__seconds = int(params["seconds"])
		self.__start = datetime.now()

		graphics.animation("success")
		self.say(f"Minuteur mis en place pour {self.__seconds} secondes")