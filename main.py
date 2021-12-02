import list

shopping_list = list.List()

import rhasspy
rhasspy.train_intent_files("sentences.ini")

while True:
	intent = rhasspy.speech_to_intent()

	action = intent["name"]
	params = intent["variables"]

	shopping_list.process(action, params)
