from entity import Entity
import sprite

class Player(Entity):
	def __init__(self):
		Entity.__init__(self, self, 0)
		self.setSpriteList(sprite.spriteLoad('sprites/retard.png'))
		self.setSprite('retard_idle')
		self.constaccel_y = 600.0
		self.accel_y = 0.0

		self.midjump = False
	def left(self, state):
		print 'left state: ', state
		if state == True:
			self.accel(-800, 0)
			self.impulse(-200, 0)
		else:
			self.accel(800, 0)
			self.impulse(200, 0)
	def right(self, state):
		print 'right state: ', state
		if state == True:
			self.accel(800, 0)
			self.impulse(200, 0)
		else:
			self.accel(-800, 0)
			self.impulse(-200, 0)
	def up(self, state):
		print 'up state: ', state
		if state == True and self.midjump == False:
			#self.midjump = True
			self.impulse(0, -250)
	def down(self, state):
		print 'down state: ', state
		if state == True:
			self.resistance_x -= 600
		else: self.resistance_x += 600
		#self.impulse(0, 100)
