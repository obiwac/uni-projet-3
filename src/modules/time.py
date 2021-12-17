import graphics
import module
from datetime import datetime

class Time(module.Module):
	def __init__(self):
		super().__init__()

	def process(self, action):
		"""
		Process potential time commands.
		"""

		if action == "Show_time":
			self.show_time()

	def show_time(self):
		"""
		Get current time, show it on screen, and read it out loud.
		"""

		now = datetime.now()
		current_time_h = now.strftime("%H")
		current_time_m = now.strftime("%M")

		graphics.text(f"{current_time_h}:{current_time_m}")
		self.say(f"Il est actuellement {current_time_h} heures {current_time_m}")
