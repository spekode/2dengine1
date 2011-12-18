from entity import TextEntity
import random

class Bouncer(TextEntity):
	def __init__(self, owner=None, layer=None):
		Entity.__init__(self, owner, layer)

		self.accel_x = random.randint(100, 800) * (random.choice[1,-1])
		self.accel_y = random.randint(100, 800) * (random.choice[1,-1])
