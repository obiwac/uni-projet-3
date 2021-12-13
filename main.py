import graphics

import rhasspy

#rhasspy.train_intent_files("sentences.ini")

import module
import modules

module.Module.rhasspy = rhasspy

shopping_list = modules.list.List()
flashy_boi = modules.flashlight.Flashlight()
the_time = modules.time.Time()
thermometer = modules.thermometer.Thermometer()
bankcode = modules.bankcode.Bankcode()

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
