import graphics
import module
import time

class Fall_detector(module.Module):
    def __init__(self):
        super().__init__()

    def update(self):
        """
        Make sure the acceleration doesn't surpass a certain magnitude.
        If it does, prompt the user for cancellation.
        If the user does not cancel within 5 seconds, scream indefinitely.
        """

        acceleration = graphics.sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        MAGNITUDE = 10

        if x > MAGNITUDE or y > MAGNITUDE or z > MAGNITUDE:
            graphics.animation("error")
            self.say("Une chute a été détéctée ; vous avez 5 secondes pour arrêter l'alarme en appuyant sur le joystick")
            time.sleep(5)
            if len(graphics.sense.stick.get_events()) == 0:
                while True:
                    self.say("alarme activée : AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
