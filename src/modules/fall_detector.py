import module
import time


class Fall_detector(module.Module):
    def __init__(self):
        super().__init__()

    def process(self, action):
        acceleration = self.sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if x > 1 or y > 1 or z > 1:

    def fall(self):
        self.show_message("Chute détectée")
        self.say("Une chute a été détéctée ; vous avez 5 secondes pour arrêter l'alarme")
        time.sleep(5)
        if len(self.sense.stick.get_events()) == 0:
            while True:
                self.say("alarme activée : AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
