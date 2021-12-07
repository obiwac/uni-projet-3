import module.list
import module.flashlight
import module.time

shopping_list = list.List(rhasspy)
flashy_boi = flashlight.Flashlight()
the_time = time.Time()

import rhasspy
rhasspy.train_intent_files("sentences.ini")

while True:
	intent = rhasspy.speech_to_intent()

	action = intent["name"]
	params = intent["variables"]

	shopping_list.process(action, params)
	flashy_boi.process(action)
	the_time.process(action)
