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

FPS = 60
CLEAN = lambda: [[(0, 0, 0) for __ in range(X_RES)] for _ in range(Y_RES)]

fb = CLEAN()

target_theta = 0
theta = 0

# load font on startup

font = {}

for i in range(0x30, 0x3a + 1):
	font[chr(i)] = Image(f"font/{hex(i)[2:]}")

def rotate_point(rotated_fb, c, s, _x, _y, colour):
	"""
	Turn a point at position (_x, _y) around the centre of the framebuffer by (c, s).
	Plot it on 'rotated_fb' with 'colour'
	"""

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
	"""
	Rotate the framebuffer by 'theta'.
	Then, flip the framebuffer to the screen and wait for 1/FPS seconds.
	"""

	rotated_fb = CLEAN()

	s = math.sin(theta)
	c = math.cos(theta)

	for y in range(Y_RES):
		for x in range(X_RES):
			rotate_point(rotated_fb, c, s, x, y, fb[y][x])

	sense.set_pixels([*chain(*rotated_fb)])
	time.sleep(1 / FPS)

events = []

def __flip_events():
	"""
	Process the joystick events.
	Concretely, this means reorienting the screen when pressing up/down/left/right by setting 'target_theta'.
	"""

	global events, target_theta

	directions = {
		"up"   : math.tau / 4 * 0,
		"right": math.tau / 4 * 1,
		"down" : math.tau / 4 * 2,
		"left" : math.tau / 4 * 3,
	}

	events = []

	for event in sense.stick.get_events():
		if event.action == "pressed":
			events.append(event.direction)

			if event.direction in directions:
				target_theta = directions[event.direction]

def flip():
	"""
	Wrapper around '__flip'.
	If 'theta' is not within a certain angle ('EPSILON') of 'target_theta', animate it.
	"""

	global target_theta, theta
	__flip_events()

	EPSILON = math.tau / 64

	while abs(target_theta - theta) > EPSILON:
		__flip()
		theta += (target_theta - theta) / FPS * 10
		__flip_events()

	__flip()

def wash(r, g, b):
	"""
	Wash the framebuffer with a certain colour.
	"""

	global fb
	fb = [[(r, g, b)] * X_RES] * Y_RES

def __image(im):
	"""
	Render an image object to the screen.
	"""

	global fb
	fb = im.pixels
	flip()

import random
from copy import deepcopy

def __scramble():
	"""
	Execute a cool and basic little animation for "scrambling" the framebuffer (Thanos snap effect).
	"""

	global fb
	nfb = deepcopy(fb)
	FAC = 1.1

	for y in range(Y_RES):
		for x in range(X_RES):
			i = x + int(random.uniform(-FAC, FAC))
			j = y + int(random.uniform(-FAC, FAC))

			if i in range(X_RES) and j in range(Y_RES):
				nfb[j][i] = tuple(map(lambda x: int(x * 0.95), fb[y][x]))

	fb = nfb

def image(path, crossed = False):
	"""
	Wrapper around '__image'.
	Load image at 'path' and render it to the screen.
	If 'crossed' is set, follow this by a call to '__scramble'.
	"""

	global fb

	im = Image(path)
	__image(im)

	if crossed:
		for _ in range(100):
			__scramble()
			flip()

def text(string):
	"""
	Scroll the text stored in 'string' across the screen.
	"""

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
	"""
	Load and render an animation.
	"""

	for i in range(4):
		image(f"{name}/{i}")
		time.sleep(0.1)

# noise code translated from C from another project of mine (the aquaBSD Installer)

NOISE_PERMUTATIONS = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]
NOISE_PERMUTATIONS *= 2

NOISE_FADE = lambda x: x ** 3 * (x * (x * 6 - 15) + 10)
NOISE_FLOOR = lambda x: int(x) if int(x) < x else int(x) - 1
NOISE_LERP = lambda x, a, b: a + x * (b - a)

def noise_gradient(hash_x, hash_y, hash_z, x, y, z):
	h = NOISE_PERMUTATIONS[hash_x + NOISE_PERMUTATIONS[hash_y + NOISE_PERMUTATIONS[hash_z]]] & 15;

	u = x if h < 8 else y
	v = y if h < 4 else (x if h in (12, 14) else z)

	return (-u if h & 1 else u) + (-v if h & 2 else v)

def noise(x, y, z):
	int_x_0, int_y_0, int_z_0 = (NOISE_FLOOR(x), NOISE_FLOOR(y), NOISE_FLOOR(z))
	int_x_1, int_y_1, int_z_1 = (int_x_0 + 1, int_y_0 + 1, int_z_0 + 1)
	
	fract_x_0, fract_y_0, fract_z_0 = (x - int_x_0, y - int_y_0, z - int_z_0)
	fract_x_1, fract_y_1, fract_z_1 = (fract_x_0 - 1, fract_y_0 - 1, fract_z_0 - 1)

	int_x_0 &= 0xFF
	int_y_0 &= 0xFF
	int_z_0 &= 0xFF

	int_x_1 &= 0xFF
	int_y_1 &= 0xFF
	int_z_1 &= 0xFF

	fade_x, fade_y, fade_z = (NOISE_FADE(fract_x_0), NOISE_FADE(fract_y_0), NOISE_FADE(fract_z_0))

	noise_x_0 = NOISE_LERP(fade_z,
		noise_gradient(int_x_0, int_y_0, int_z_0, fract_x_0, fract_y_0, fract_z_0),
	    noise_gradient(int_x_0, int_y_0, int_z_1, fract_x_0, fract_y_0, fract_z_1));

	noise_x_1 = NOISE_LERP(fade_z,
		noise_gradient(int_x_0, int_y_1, int_z_0, fract_x_0, fract_y_1, fract_z_0),
		noise_gradient(int_x_0, int_y_1, int_z_1, fract_x_0, fract_y_1, fract_z_1));

	noise_0 = NOISE_LERP(fade_y, noise_x_0, noise_x_1);

	noise_x_0 = NOISE_LERP(fade_z,
		noise_gradient(int_x_1, int_y_0, int_z_0, fract_x_1, fract_y_0, fract_z_0),
	    noise_gradient(int_x_1, int_y_0, int_z_1, fract_x_1, fract_y_0, fract_z_1));

	noise_x_1 = NOISE_LERP(fade_z,
		noise_gradient(int_x_1, int_y_1, int_z_0, fract_x_1, fract_y_1, fract_z_0),
		noise_gradient(int_x_1, int_y_1, int_z_1, fract_x_1, fract_y_1, fract_z_1));

	noise_1 = NOISE_LERP(fade_y, noise_x_0, noise_x_1);

	return NOISE_LERP(fade_x, noise_0, noise_1) * 0.936 # 3D noise rescaling factor

__t = 0 # time in seconds elapsed

def rainbow(name):
	"""
	Render an image filled with a certain colour based on the above noise function.
	"""

	global fb, __t

	im = Image(name)
	fb = CLEAN()

	scale = X_RES / 1.5
	__t += 1 / FPS * 3

	for y in range(Y_RES):
		for x in range(X_RES):
			r = 1.0 # noise(x / scale, y / scale, __t + 0000) / 2 + 0.5
			g = noise(x / scale, y / scale, __t + 1000) / 2 + 0.5
			b = noise(x / scale, y / scale, __t - 1000) / 2 + 0.5

			if im.pixels[y][x][0]:
				fb[y][x] = tuple(map(lambda x: int(x * 0xFF), (r, g, b)))

	flip()