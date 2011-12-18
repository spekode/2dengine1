from entity import TextEntity
import sprite
from timer import Timer
from scene import getScene
import random

class Bullet(TextEntity):
	def __init__(self, owner, layer, vel_x, vel_y):
		TextEntity.__init__(self, owner, layer, char = '+')
		self.setPos(owner.pos_x, owner.pos_y)
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.visible = True
		self.liveTimer = Timer()
		self.liveTimer.start()
	
	def death(self, attacker=None, deathtype=None):
		self.health = -1

	def think(self, frameDT):
		if self.liveTimer.elapsed() > 1000:
			self.health = 0

		if not self.health:
			self.death()

class Fuzzie(TextEntity):
	def __init__(self, layer, vel_x, vel_y):
		TextEntity.__init__(self, self, layer, char = '*')
		#self.setPos(self.pos_x, s.pos_y)
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.visible = True
		self.liveTimer = Timer()
		self.liveTimer.start()
	
	def death(self, attacker=None, deathtype=None): pass

	def think(self, frameDT): pass

class Player(TextEntity):
	def __init__(self):
		TextEntity.__init__(self, self, 0)
		self.rateOfFire = 250
		self.shooting = False
		self.shootingTime = Timer().start()
		self.fire_x = 0
		self.fire_y = 0
		self.fire_vel = 100

		self.levelMax = 20
		self.levelCur = 0 
		self.levelFuzzieEx = 2 #Chance of a fuzzie spawning during the time (20% chance)

		#self.constaccel_y = 600.0
		#self.vel_x_max = 100.0
		#self.vel_y_max = 100.0
#		self.accel_y = 0.0
		#self.resistance_x = 1.0
	def left(self, key, state):
		if state == True:
			self.accel(-10, 0)
			self.impulse(-15, 0)
		else:
			self.accel(10, 0)
			self.impulse(15, 0)
	def right(self, key, state):
		if state == True:
			self.accel(10, 0)
			self.impulse(15, 0)
		else:
			self.accel(-10, 0)
			self.impulse(-15, 0)
	def up(self, key, state):
		if state == True:
			self.accel(0, -10)
			self.impulse(0, -15)
		else:
			self.accel(0, 10)
			self.impulse(0, 15)				
	def down(self, key, state):
		# POWER SLIDE!!!
		#if state == True:
		#	self.resistance_x -= 600
		#else: self.resistance_x += 600
		if state == True:
			self.accel(0, 10)
			self.impulse(0, 15)
		else:
			self.accel(0, -10)
			self.impulse(0, -15)

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

		if random.randint(1,self.levelFuzzieEx*30) == 1 and self.levelCur <= self.levelMax: #CHANCE*CURRENT_FPS should do the trick...
			getScene().add(Fuzzie(4, 50, 2), 4)
			self.levelCur += 1