
import module
from sense_hat import SenseHat

sense = SenseHat()

class Thermometer(module.Module):
	def __init__(self, rhasspy):
		super().__init__(rhasspy)

		X =(255, 255, 255) #blanc
		B =(0, 0, 255) #bleu
		O =(0,0,0) #nothing
		Y =(210,105,30) #brun
		self.boire_eau=[
		O, O, O, O, O, O, O, O,
		O, O, X, O, O, X, O, O,
		O, O, X, B, B, X, O, O,
		O, O, X, B, B, X, O, O,
		O, O, X, B, B, X, O, O,
		O, O, X, B, B, X, O, O,
		O, O, X, X, X, X, O, O,
		O, O, O, O, O, O, O, O
		]
		self.boire_chaud=[
		O, O, O, O, O, O, O, O,
		O, O, O, O, O, X, O, O,
		O, O, O, O, X, O, O, O,
		O, O, X, Y, Y, X, O, O,
		O, O, X, Y, Y, X, X, O,
		O, O, X, Y, Y, X, O, O,
		O, O, O, X, X, O, O, O,
		O, O, O, O, O, O, O, O
		]
	
	def temperature_from_pressure(self):
		temp = sense.get_temperature_from_pressure()
		self.say(f"Il fait {round(temp)} degrés celsius")
		if temp >= 25 :
			sense.set_pixels(self.boire_eau)
			self.say("Il fait chaud, pensez à boire")
		elif temp <= 0 :
			sense.set_pixels(self.boire_chaud)
			self.say("Il fait froid, buvez quelque chose de chaud")

	def process(self, action, params):
		if action == "Tell_temperature":
			self.temperature_from_pressure()
