
import graphics
import module

class Thermometer(module.Module):
	def __init__(self):
		super().__init__()
	
	def temperature_from_pressure(self):
		temp = graphics.sense.get_temperature()
		graphics.text(str(int(round(temp))))
		self.say(f"Il fait {round(temp)} degrés celsius")
		if temp >= 25 :
			graphics.image("items/bière")
			self.say("Il fait chaud, pensez à boire")
		elif temp <= 0 :
			graphics.image("items/café")
			self.say("Il fait froid, buvez quelque chose de chaud")

	def process(self, action, params):
		if action == "Tell_temperature":
			self.temperature_from_pressure()
