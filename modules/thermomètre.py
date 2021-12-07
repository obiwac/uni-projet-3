
class thermometre():
    def __init__(self):
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
        sense = SenseHat()
        self.temp = sense.get_temperature_from_pressure()
        text_to_speech("Temperature: %s C" % temp)
        if sense.get_temperature_from_pressure() >= 25 :
            text_to_speech("Rappel : forte chaleur, pensez à boire")
            sense.set_pixels(self.boire_eau)
        elif sense.get_temperature_rom_pressure() <= 0 :
            text_to_speech("Rappel : faible chaleur, buvez quelque chose de chaud")
            sense.set_pixels(self.boire_chaud)
        
        