from sense_hat import SenseHat


s = SenseHat()

class Flashlight:

    def process(self, action):
        if action == "Flashlight_on":
            self.turn_on()
        elif action == "Flashlight_off":
            self.turn_off()
        
    def turn_on():
        O = [255, 255, 255]  # White
        led_status = [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O
        ]
        s.set_pixels(led_status)
        
    def turn_off():
        a = [0,0,0]
        led_status = [
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        a, a, a, a, a, a, a, a,
        ]
        s.set_pixels(led_status)
