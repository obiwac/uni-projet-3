import graphics
import module

class Flashlight(module.Module):
	def __init__(self):
		super().__init__()

	def process(self, action):
		exported = {
			"Flashlight_on": self.turn_on,
			"Flashlight_off": self.turn_off
		}

		if action in exported:
			exported[action]()

	def turn_on(self):
		graphics.wash(255, 255, 255)
		graphics.flip()
		self.say("Lampe torche allumée")
        
	def turn_off(self):
		self.wash(0, 0, 0)
		graphics.flip()
		graphics.say("Lampe torche éteinte")
