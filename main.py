import rhasspy
#rhasspy.train_intent_files("sentences.ini")

import modules

shopping_list = modules.list.List(rhasspy)
flashy_boi = modules.flashlight.Flashlight()

while True:
	intent = rhasspy.speech_to_intent()
	print(intent)

	action = intent["name"]
	params = intent["variables"]

	shopping_list.process(action, params)
	flashy_boi.process(action)
	the_time.process(action)
