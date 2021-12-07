from datetime import datetime
now = datetime.now()
from sense_hat import SenseHat
s = SenseHat()

class Time:

    def process(self, action):
        if action == "Show_time":
            self.show_time()


    def show_time():
        current_time_h = now.strftime("%H")
        current_time_m = now.strftime("%M")
        s.show_message(f"{current_time_h}:{current_time_m}")
        s.text_to_speech(f"Il est actuellement {current_time_h} heures {current_time_m}")



    