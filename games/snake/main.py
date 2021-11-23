import sense_hat
import random
import time

GAME_X = 8
GAME_Y = 8

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

# snake linked list node

class Snake_bit:
	def __init__(self, x, y, next = None):
		self.next = next

		self.x = x
		self.y = y

class Game:
	def __init__(self):
		self.sense = sense_hat.SenseHat()

		self.running = True
		self.score = 0

		self.dir = None # current direction

		self.snake = Snake_bit(GAME_X // 2, GAME_Y // 2)
		self.place_apple()

	def place_apple(self):
		self.apple_x = random.randint(0, GAME_X - 1)
		self.apple_y = random.randint(0, GAME_Y - 1)

		# TODO make sure we don't place an apple over a bit of snake

	def update(self):
		# process events

		prev_dir = self.dir

		for event in self.sense.stick.get_events():
			if event.action == "pressed":
				if event.direction == "up": self.dir = DIR_UP
				elif event.direction == "right": self.dir = DIR_RIGHT
				elif event.direction == "down": self.dir = DIR_DOWN
				elif event.direction == "left": self.dir = DIR_LEFT

		if prev_dir is not None and self.dir % 2 == prev_dir % 2:
			self.dir = prev_dir

		if self.dir is None:
			return

		# move the head in the current direction of movement

		prev_head = self.snake
		head = Snake_bit(prev_head.x, prev_head.y, next = prev_head)

		if game.dir == DIR_UP: head.y -= 1
		elif game.dir == DIR_DOWN: head.y += 1
		elif game.dir == DIR_LEFT: head.x -= 1
		elif game.dir == DIR_RIGHT: head.x += 1

		# calculate intersection with sides of playfield

		intersection = head.x in (-1, GAME_X) or head.y in (-1, GAME_Y)

		if intersection:
			head.x = prev_head.x
			head.y = prev_head.y

		self.snake = head

		# calculate self-intersection, and while we're at it, get the last bit of snake

		last = head

		while last.next.next:
			last = last.next
			intersection |= last.x == head.x and last.y == head.y

		if intersection:
			self.running = False
			return

		# are we on an apple?

		if head.x != self.apple_x or head.y != self.apple_y:
			last.next = None
			return

		self.score += 1
		self.place_apple()

	def render(self):
		self.sense.clear()
		self.sense.set_pixel(self.apple_x, self.apple_y, 255, 0, 255)

		bit = self.snake

		while bit:
			self.sense.set_pixel(bit.x, bit.y, 0, 255, 0)
			bit = bit.next

	def run(self):
		while self.running:
			time.sleep(0.5 - self.score / 50)

			game.update()
			game.render()

		self.sense.show_message(f"Score: {self.score}")

if __name__ == "__main__":
	game = Game()
	game.run()
