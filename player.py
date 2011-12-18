from entity import TextEntity
import sprite
from timer import Timer
from scene import getScene
import random

class Bullet(TextEntity):
	def __init__(self, owner, layer, vel_x, vel_y):
		TextEntity.__init__(self, owner, layer, char = '+')
		self.setPos(owner.pos_x, owner.pos_y)
		self.setOldPos(owner.pos_x, owner.pos_y)
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.visible = True
		self.liveTimer = Timer()
		self.liveTimer.start()
		self.name = 'Bullet'
	
	def death(self, attacker=None, deathtype=None):
		self.health = -1

	def collide(self, partners):
		for partner in partners:
			if partner[0]:
				if partner[0] == self.owner:
					pass # we don't hurt ourselves :D
			else:
				# hit the map
				#print "hit a wall"
				self.pos_x = self.oldpos_x
				self.pos_y = self.oldpos_y
				self.vel_x = 0
				self.vel_y = 0
				self.health = 0

	def think(self, frameDT):
		if self.liveTimer.elapsed() > 1000:
			#print "timed out!"
			self.health = 0

		if not self.health:
			#print "died!"
			self.death()

class Fuzzie(TextEntity):
	def __init__(self, layer, vel_x, vel_y):
		TextEntity.__init__(self, None, layer, char = '*')
		#self.setPos(self.pos_x, s.pos_y)
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.visible = True
		self.liveTimer = Timer()
		self.liveTimer.start()
		self.name = 'Fuzzie'
	
	def death(self, attacker=None, deathtype=None): pass

	def think(self, frameDT): pass

	def collide(self, partners):
		for partner in partners:
			if partner[0]:
				if partner[0].char == '+':
					self.health = 0
		
			else:
				self.pos_x = self.oldpos_x
				self.pos_y = self.oldpos_y
				self.vel_x = 0
				self.vel_y = 0

MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 4
MOVE_DOWN = 8

class Player(TextEntity):
	def __init__(self):
		TextEntity.__init__(self, self, 0)
		self.rateOfFire = 250
		self.shooting = False
		self.shootingTime = Timer().start()
		self.fire_x = 0
		self.fire_y = 0
		self.fire_vel = 100
		self.name = 'Player'

		self.moveRate = 50
		self.moving = False
		self.moveTime = Timer().start()
		self.move_vel = 7

		self.vel_y_max = 10
		self.vel_x_max = 10
		self.resistance_x = 35.0
		self.resistance_y = 35.0

		self.levelMax = 20
		self.levelCur = 0 
		self.levelFuzzieEx = 2 #Chance of a fuzzie spawning during the time (20% chance)

		#self.constaccel_y = 20.0
		#self.vel_x_max = 100.0
		#self.vel_y_max = 100.0
#		self.accel_y = 0.0
		#self.resistance_x = 1.0
	def left(self, key, state):
		if state == True:
			self.moving |= MOVE_LEFT
		else:
			self.moving &= ~MOVE_LEFT
	def right(self, key, state):
		if state == True:
			self.moving |= MOVE_RIGHT
		else:
			self.moving &= ~MOVE_RIGHT
	def up(self, key, state):
		if state == True:
			self.moving |= MOVE_UP
		else:
			self.moving &= ~MOVE_UP
	def down(self, key, state):
		# POWER SLIDE!!!
		#if state == True:
		#	self.resistance_x -= 600
		#else: self.resistance_x += 600
		if state == True:
			self.moving |= MOVE_DOWN
		else:
			self.moving &= ~MOVE_DOWN

	def _move(self):
		if self.moveTime.elapsed() < self.moveRate:
			return
		
		x = y = 0
		if self.moving & MOVE_LEFT: x -= self.move_vel
		if self.moving & MOVE_RIGHT: x += self.move_vel
		if self.moving & MOVE_UP: y -= self.move_vel
		if self.moving & MOVE_DOWN: y += self.move_vel
		
		self.impulse(x, y)
		self.moveTime.restart()

	def _fire(self, x, y):
		if self.shootingTime.elapsed() < self.rateOfFire:
			return
		if not x and not y: return

		getScene().add(Bullet(self, 3, x, y), 3)
		self.shootingTime.restart()

	def fireUp(self, key, state): 
		if self.shooting and not state:
			self.shooting -= 1
			self.fire_y += self.fire_vel
		elif state == True:
			self.shooting += 1
			self.fire_y += -self.fire_vel
	def fireDown(self, key, state):
		if self.shooting and not state:
			self.shooting -= 1
			self.fire_y -= self.fire_vel
		elif state == True:
			self.shooting += 1
			self.fire_y += self.fire_vel
	def fireLeft(self, key, state):
		if self.shooting and not state:
			self.shooting -= 1
			self.fire_x += self.fire_vel
		elif state == True:
			self.shooting += 1
			self.fire_x += -self.fire_vel
	def fireRight(self, key, state):
		if self.shooting and not state:
			self.shooting -= 1
			self.fire_x -= self.fire_vel
		elif state == True:
			self.shooting += 1
			self.fire_x += self.fire_vel

	def think(self, frameDT):
		if self.shooting > 0:
			self._fire(self.fire_x, self.fire_y)
		if self.moving:
			self._move()

		if random.randint(1,self.levelFuzzieEx*30) == 1 and self.levelCur <= self.levelMax: #CHANCE*CURRENT_FPS should do the trick...
			getScene().add(Fuzzie(10, 30, 30), 4)
			self.levelCur += 1