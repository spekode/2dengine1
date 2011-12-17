from entity import Entity
from text import TextCharacter
import sprite

class Player(Entity):
	def __init__(self):
		Entity.__init__(self, self, 0)
		self.setSpriteList(sprite.spriteLoad('sprites/retard.png'))
		self.setSprite('retard_idle')
		#self.constaccel_y = 600.0
		self.accel_y = 0.0
		self.character = TextCharacter()
		self.character.setChar('@')

		self.midjump = False
	def left(self, key, state):
		if state == True:
			self.accel(-800, 0)
			self.impulse(-200, 0)
		else:
			self.accel(800, 0)
			self.impulse(200, 0)
	def right(self, key, state):
		if state == True:
			self.accel(800, 0)
			self.impulse(200, 0)
		else:
			self.accel(-800, 0)
			self.impulse(-200, 0)
	def up(self, key, state):
		if state == True:
			self.accel(0, -800)
			self.impulse(0, -250)
		else:
			self.accel(0, 800)
			self.impulse(0, 250)
						
	def down(self, key, state):
		# POWER SLIDE!!!
		#if state == True:
		#	self.resistance_x -= 600
		#else: self.resistance_x += 600

		if state == True:
			self.accel(0, 800)
			self.impulse(0, 200)
		else:
			self.accel(0, -800)
			self.impulse(0, -200)

	def draw(self, frameDT, surface, x, y):
		if self.visible:
			self.character.draw(surface, frameDT, x, y)