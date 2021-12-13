# this file handles all that is related to drawing graphics/text to the screen
# it uses the sense_hat module for its output, which uses a global state
# because of this, the functions can/need to be static, so no point putting them in a class

import math # for trig functions
from sense_hat import SenseHat

X_RES = 8
Y_RES = 8

sense = sense_hat.SenseHat()

CLEAN = lambda: [[(0, 0, 0)] * X_RES] * Y_RES

fb = CLEAN()

target_theta = 0
theta = 0

def rotate_point(rotated_fb, c, s, x, y, colour):
	x -= X_RES // 2
	y -= Y_RES // 2

	x = int(x * c - y * s)
	y = int(x * s + y * c)

	try:
		rotated_fb[x][y] = colour

	except IndexError:
		pass

def flip():
	global theta
	rotated_fb = CLEAN()

	# TODO change theta based on orientation here
	theta += (target_theta - target) / 10

	s = math.sin(theta)
	c = math.cos(theta)

	for y in range(Y_RES):
		for x in range(X_RES):
			rotate_point(rotated_fb, c, s, x, y, fb[x][y])
			colour = fb[x][y]

	self.sense.set_pixels(rotated_fb)

def render():
	flip()

def wash(r, g, b):
	global fb
	fb = [[(r, g, b)] * X_RES] * Y_RES
