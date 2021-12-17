import graphics
import rhasspy

rhasspy.train_intent_files("sentences.ini")

# modules

import module
import modules

module.Module.rhasspy = rhasspy

# say hello to the user!

graphics.animation("success")
rhasspy.text_to_speech("Bonjour")

# instantiate all our modules

shopping_list = modules.list.List()
flashy_boi = modules.flashlight.Flashlight()
the_time = modules.time.Time()
thermometer = modules.thermometer.Thermometer()
bankcode = modules.bankcode.Bankcode()
fall_detector = modules.fall_detector.Fall_detector()
timer = modules.timer.Timer()

# games

import games.snake as snake

# main loop

while True:
	# while the middle button is not pressed on the joystick, continuously update the fall detector and timer
	# also, render the smile with the kinda rainbow animation

	while "middle" not in graphics.events:
		fall_detector.update()
		timer.update()
		graphics.rainbow("smile")

	# when user presses the joystick button, await speech

	graphics.animation("mic")
	intent = rhasspy.speech_to_intent()
	print(intent)

	action = intent["name"]
	params = intent["variables"]

	# snake game

	if action == "Game_snake":
		graphics.animation("success")

		game = snake.Game()
		score = game.run()
		
		graphics.text(str(score))
		rhasspy.text_to_speech(f"Vous avez obtenu un score de {score}")

		continue

	# make each module process the action

	shopping_list.process(action, params)
	flashy_boi.process(action)
	the_time.process(action)
	thermometer.process(action, params)
	bankcode.process(action, params)
	timer.process(action, params)