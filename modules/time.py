from datetime import datetime
from sense_hat import SenseHat
s = SenseHat()

class Time(Module):
	def __init__(self, rhasspy):
		super().__init__(rhasspy)

    def process(self, action):
        if action == "Show_time":
            self.show_time()

    def show_time(self):
		now = datetime.now()
        current_time_h = now.strftime("%H")
        current_time_m = now.strftime("%M")

        s.show_message(f"{current_time_h}:{current_time_m}")
        self.say(f"Il est actuellement {current_time_h} heures {current_time_m}")
