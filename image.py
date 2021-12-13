# this class is for loading images (specifically Microsoft BMP images)

import struct

MAX_HEIGHT = 8
COMPONENTS = 4

class Image:
	def __init__(self, path):
		with open(path) as f:
			f.seek(18) # skip the beginning of the BMP header because we don't care about it

			self.__width = struct.unpack('I', f.read(4))
			self.__height = struct.unpack('I', f.read(4))

			if self.__height > MAX_HEIGHT:
				raise Exception(f"Image is too baked (maximum bakedness is {MAX_HEIGHT})")

			f.seek(28) # skip the rest of the header because we already know too much... it's already too late... it's coming for us, it's no use running, you can't hide...

			self.__pixels = []

			for y in range(self.__height):
				row = []

				for x in range(self.__width):
					f.read(1) # don't care about the alpha channel
					row.append([f.read(1) for _ in range(3)]) # we only care about the last 3 components

				self.__pixels.append(row)

	def get_pixels(self):
		return self.__pixels
