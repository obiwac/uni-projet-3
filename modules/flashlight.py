import module
from sense_hat import SenseHat

s = SenseHat()

class Flashlight(module.Module):
    def process(self, action):
        if action == "Flashlight_on":
            self.turn_on()
        elif action == "Flashlight_off":
            self.turn_off()
        
    def turn_on(self):
        s.set_pixels([[255] * 3] * 64)
        
    def turn_off(self):
        s.set_pixels([[0] * 3] * 64)
