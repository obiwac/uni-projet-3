
import module
from sense_hat import SenseHat

sense = SenseHat()

class Thermometer(Module):
    def __init__(self, rhasspy):
		super().__init__(rhasspy)

        X =(255, 255, 255) #blanc
        B =(0, 0, 255) #bleu
        O =(0,0,0) #nothing
        Y (210,105,30) #brun
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
        self.temp = sense.get_temperature_from_pressure()
        self.say(f"Il fait {temp:02f} degrés celsius")
        if self.temp >= 25 :
            self.say("Il fait chaud, pensez à boire")
            sense.set_pixels(self.boire_eau)
        elif self.temp <= 0 :
            self.say("Il fait froid, buvez quelque chose de chaud")
            sense.set_pixels(self.boire_chaud)

	def process(self, action, params):
		if action == "Tell_temperature":
			self.temperature_from_pressure()
