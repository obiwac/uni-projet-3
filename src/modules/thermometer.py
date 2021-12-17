
import graphics
import module

class Thermometer(module.Module):
	def __init__(self):
		super().__init__()
	
	def temperature_from_pressure(self):
		"""
		Get temperature from pressure sensor.
		Show the degrees celsius on screen and say it out loud.
		If it's too hot or too cold, notify the user.
		"""

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
		"""
		Process potential thermometer commands.
		"""

		if action == "Tell_temperature":
			self.temperature_from_pressure()
