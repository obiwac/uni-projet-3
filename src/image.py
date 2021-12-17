# this class is for loading images (specifically Microsoft BMP images)

import struct

MAX_HEIGHT = 8

class Image:
	def __init__(self, path):
		"""
		Load BMP image from 'path'.
		"""

		path = f"images/{path}.bmp"

		# 'rb' mode so that we can parse with 'struct'

		with open(path, "rb") as f:
			f.seek(18) # skip the beginning of the BMP header because we don't care about it

			self.__width ,= struct.unpack('I', f.read(4))
			self.__height ,= struct.unpack('I', f.read(4))

			if self.__height > MAX_HEIGHT:
				raise Exception(f"Image is too baked (maximum bakedness is {MAX_HEIGHT})")

			f.read(2) # skip colour planes
			alpha = struct.unpack('H', f.read(2))[0] == 32

			f.seek(137 + (not alpha)) # skip the rest of the header because we already know too much... it's already too late... it's coming for us, it's no use running, you can't hide...

			self.pixels = []

			for y in range(self.__height):
				row = []

				for x in range(self.__width):
					if alpha:
						f.read(1) # we only care about the last 3 components

					colour = struct.unpack('BBB', f.read(3))
					row.append(colour[::-1])

				self.pixels.append(row)

			self.pixels = self.pixels[::-1]
