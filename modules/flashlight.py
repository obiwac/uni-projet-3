import module

class Flashlight(module.Module):
	def __init__(self):
		super().__init__()

    def process(self, action):
		exported = {
			"Flashlight_on": self.turn_on,
			"Flashlight_off": self.turn_off
		}

		exported[action]()

    def turn_on(self):
		self.say("Lampe torche allumée")
        self.wash(255, 255, 255)
        
    def turn_off(self):
		self.say("Lampe torche éteinte")
        self.wash(0, 0, 0)
