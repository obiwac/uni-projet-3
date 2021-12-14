import graphics
import rhasspy

#rhasspy.train_intent_files("sentences.ini")

# modules

import module
import modules

module.Module.rhasspy = rhasspy
graphics.animation("success")
rhasspy.text_to_speech("Bonjour")

shopping_list = modules.list.List()
flashy_boi = modules.flashlight.Flashlight()
the_time = modules.time.Time()
thermometer = modules.thermometer.Thermometer()
bankcode = modules.bankcode.Bankcode()

# games

import games.snake as snake

while True:
	while "middle" not in graphics.events:
		graphics.rainbow("smile")

	graphics.animation("mic")
	intent = rhasspy.speech_to_intent()
	print(intent)

	action = intent["name"]
	params = intent["variables"]

	if action == "Game_snake":
		graphics.animation("success")

		game = snake.Game()
		score = game.run()
		
		graphics.text(str(score))
		rhasspy.text_to_speech(f"Vous avez obtenu un score de {score}")

		continue

	shopping_list.process(action, params)
	flashy_boi.process(action)
	the_time.process(action)
	thermometer.process(action, params)
	bankcode.process(action, params)
