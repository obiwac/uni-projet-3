# this file handles all that is related to drawing graphics/text to the screen
# it uses the sense_hat module for its output, which uses a global state
# because of this, the functions can/need to be static, so no point putting them in a class

import image
import math # for trig functions
import sense_hat

X_RES = 8
Y_RES = 8

sense = sense_hat.SenseHat()

CLEAN = lambda: [[(0, 0, 0)] * X_RES] * Y_RES

fb = CLEAN()

target_theta = 0
theta = 0

# load font on startup

font = {}

for i in range(0x30, 0x3a + 1):
	font[chr(i)] = image.Image(f"font/{hex(i)[2:]}")

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

def wash(r, g, b):
	global fb
	fb = [[(r, g, b)] * X_RES] * Y_RES

def image(path, crossed = False):
	global fb

	if crossed:
		print("TODO graphics image crossed")

	image = image.Image(path)
	fb = image.pixels
	flip()

def text(string):
	global fb

	buf = [[] for _ in range(Y_RES)]

	for char in string:
		for y in range(8):
			row = buf[y]
			row.extend(font[char].pixels[y])

	# scroll text

	for x in range(len(buf[0]) - X_RES):
		for y, row in enumerate(buf):
			fb[y] = row[x: x + X_RES]

		flip()

# preset animations

def cancel():
	print("TODO cancel animation")

def question():
	print("TODO question mark animation")

def microphone():
	print("TODO microphone animation")

def error():
	print("TODO error animation")

def success():
	print("TODO success animation")

def lock():
	print("TODO lock animation")

def unlock():
	print("TODO unlock animation")
