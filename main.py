import list

import rhasspy
rhasspy.train_intent_files("sentences.ini")

shopping_list = list.List(rhasspy)

while True:
	intent = rhasspy.speech_to_intent()

	action = intent["name"]
	params = intent["variables"]

	shopping_list.process(action, params)
