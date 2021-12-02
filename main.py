import list
import flashlight

shopping_list = list.List()
flashy_boi = flashlight.Flashlight()

import rhasspy
rhasspy.train_intent_files("sentences.ini")

while True:
	intent = rhasspy.speech_to_intent()

	action = intent["name"]
	params = intent["variables"]

	shopping_list.process(action, params)
	flashy_boi.process(action)
