import sense_hat

TAU = 6.28
SIXTH = TAU / 6

sense = sense_hat.SenseHat()

def render_smiley(hue):
	global sense

	# convert HSV to RGB (saturation and value are assumed to be 1)

	hue %= TAU
	x = 1 - abs(hue / SIXTH % 2 - 1)

	lut = ((1, x, 0), (x, 1, 0), (0, 1, x), (0, x, 1), (x, 0, 1), (1, 0, x))
	colour = lut[int(hue / SIXTH)]

	# display image

	O = [0, 0, 0]
	X = list(map(lambda x: int(x * 0xFF), colour))
  
	image = [
		O, O, O, O, O, O, O, O,
		O, O, X, O, O, X, O, O,
		O, O, X, O, O, X, O, O,
		O, O, X, O, O, X, O, O,
		O, O, O, O, O, O, O, O,
		O, X, O, O, O, O, X, O,
		O, O, X, X, X, X, O, O,
		O, O, O, O, O, O, O, O
	]
  
	sense.set_pixels(image)

hue = 0

while 1:
	render_smiley(hue)
	hue += TAU / 360
