# this file handles all that is related to drawing graphics/text to the screen
# it uses the sense_hat module for its output, which uses a global state
# because of this, the functions can/need to be static, so no point putting them in a class

from itertools import chain
from image import Image
import math # for trig functions
import time
import sense_hat

X_RES = 8
Y_RES = 8

sense = sense_hat.SenseHat()

CLEAN = lambda: [[(0, 0, 0) for __ in range(X_RES)] for _ in range(Y_RES)]

fb = CLEAN()

target_theta = 0
theta = 0

# load font on startup

font = {}

for i in range(0x30, 0x3a + 1):
	font[chr(i)] = Image(f"font/{hex(i)[2:]}")

def rotate_point(rotated_fb, c, s, _x, _y, colour):
	_x -= X_RES // 2 - 0.5
	_y -= Y_RES // 2 - 0.5

	x = _x * c - _y * s
	y = _x * s + _y * c

	x += X_RES // 2 - 0.5
	y += Y_RES // 2 - 0.5

	x = round(x) // 1
	y = round(y) // 1

	try:
		rotated_fb[y][x] = colour

	except IndexError:
		pass

def __flip():
	rotated_fb = CLEAN()

	s = math.sin(theta)
	c = math.cos(theta)

	for y in range(Y_RES):
		for x in range(X_RES):
			rotate_point(rotated_fb, c, s, x, y, fb[y][x])

	sense.set_pixels([*chain(*rotated_fb)])

def __flip_events():
	global target_theta

	directions = {
		"up"   : math.tau / 4 * 0,
		"right": math.tau / 4 * 1,
		"down" : math.tau / 4 * 2,
		"left" : math.tau / 4 * 3,
	}

	for event in sense.stick.get_events():
		if event.action == "pressed":
			if event.direction in directions:
				target_theta = directions[event.direction]

def flip():
	global target_theta, theta
	__flip_events()

	while abs(target_theta - theta) > math.tau / 64:
		__flip()
		theta += (target_theta - theta) / 60 * 10
		time.sleep(1 / 60) # 60 fps
		__flip_events()

	__flip()

def wash(r, g, b):
	global fb
	fb = [[(r, g, b)] * X_RES] * Y_RES

def image(path, crossed = False):
	global fb

	if crossed:
		print("TODO graphics image crossed")

	im = Image(path)
	fb = im.pixels
	flip()

def text(string):
	global fb

	buf = [[] for _ in range(Y_RES)]

	for char in string:
		for y in range(8):
			row = buf[y]
			row.extend(map(lambda x: (x[1],) * 3, font[char].pixels[y]))

	# scroll text

	for x in range(len(buf[0]) - X_RES + 1):
		for y, row in enumerate(buf):
			fb[y] = row[x: x + X_RES]

		time.sleep(0.1)
		flip()

def animation(name):
	for i in range(4):
		image(f"{name}/{i}")
		time.sleep(0.2)
