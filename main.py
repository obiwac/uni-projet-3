import rhasspy
#rhasspy.train_intent_files("sentences.ini")

import modules

shopping_list = modules.list.List(rhasspy)
flashy_boi = modules.flashlight.Flashlight()
the_time = modules.time.Time(rhasspy)
thermometer = modules.thermometer.Thermometer(rhasspy)
bankcode = modules.bankcode.Bankcode(rhasspy)

while True:
	intent = rhasspy.speech_to_intent()
	print(intent)

	action = intent["name"]
	params = intent["variables"]

	shopping_list.process(action, params)
	flashy_boi.process(action)
	the_time.process(action)
	thermometer.process(action, params)
	bankcode.process(action, params)
