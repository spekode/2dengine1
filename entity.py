def LinearChange(rate, currentTime, currentDelta):
	return rate * (currentDelta/1000)

class Entity(object):
	def __init__(self, owner=None, layer=None):
		self.owner = owner # If this belongs to a player, player goes here
		self.layer = layer # The layer this belongs to

		self.sprite = None # The current sprite object
		self.sprites = None # The available sprites

		self.vel_x_max = 300
		self.vel_y_max = 300

		self.accel_x = 0.0
		self.accel_y = 0.0
		self.pos_x = 0.0
		self.pos_y = 0.0
		self.vel_x = 0.0
		self.vel_y = 0.0
		self.constaccel_x = 0.0
		self.constaccel_y = 0.0
		self.resistance_x = 10.0
		self.resistance_y = 10.0
		self.rotation = 0.0
		
		self.colRect = None
		self.colCircle = None

		self.health = 0
		self.visible = False

		self.touching = []

	# Actions (most likely overriden by a subclass)
	def think(self): pass

	def accel(self, x, y, tlen=None, tfunc=LinearChange):
		self.accel_x += x
		self.accel_y += y
	def rotateLeft(self, rads, tlen=None, tfunc=LinearChange): pass
	def rotateRight(self, rads, tlen=None, tfunc=LinearChange): pass
	def attack1(self): pass
	def attack2(self): pass
	def block(self): pass

	def impulse(self, x=0, y=0):
		self.vel_x += x
		self.vel_y += y
	def collide(self, partners=[]): pass
	def takeDamage(self, attacker, dmg, dmgtype=None): pass
	def death(self, attacker, deathtype=None): pass
	def respawn(self): pass

	def draw(self, frameDT, surface, x, y):
		if self.visible and self.sprite:
			self.sprite.draw(frameDT, surface, x, y)

	def move(self, frameDT):
		frameDTfract = frameDT/1000
		# Apply acceleration
		self.vel_x += (self.accel_x * frameDTfract) + (self.constaccel_x * frameDTfract)
		self.vel_y += (self.accel_y * frameDTfract) + (self.constaccel_y * frameDTfract)

		# Apply resistance on X axis
		if self.vel_x > 0:
			self.vel_x -= self.resistance_x * frameDTfract
			if self.vel_x < 0: self.vel_x = 0
		elif self.vel_x < 0:
			self.vel_x += self.resistance_x * frameDTfract
			if self.vel_x > 0: self.vel_x = 0
		# Apply resistance on Y axis
		if self.vel_y > 0:
			self.vel_y -= self.resistance_y * frameDTfract
			if self.vel_y < 0: self.vel_y = 0
		elif self.vel_y < 0:
			self.vel_y += self.resistance_y * frameDTfract
			if self.vel_y > 0: self.vel_y = 0

		# Limit velocity
		if self.vel_x_max:
			if self.vel_x > self.vel_x_max: self.vel_x = self.vel_x_max
			elif self.vel_x < -self.vel_x_max: self.vel_x = -self.vel_x_max
		if self.vel_y_max:
			if self.vel_y > self.vel_y_max: self.vel_y = self.vel_y_max
			elif self.vel_y < -self.vel_y_max: self.vel_y = -self.vel_y_max		# Update position
		self.pos_x += self.vel_x * frameDTfract
		self.pos_y += self.vel_y * frameDTfract

		# Contain entity within an area (default is playfield)
		self.respectBoundry()

	def respectBoundry(self):
		if self.pos_y < 0: self.pos_y = 0
		elif self.pos_y > 4096: self.pos_y = 4096
		if self.pos_x < 0: self.pos_x = 0
		elif self.pos_x > 4096: self.pos_x = 4096

	def setSpriteList(self, sprites):
		self.sprites = sprites

	def setSprite(self, spritename):
		if self.sprites:
			self.sprite = self.sprites.get(spritename)
			self.sprite.reset()

	# Easymodes
	def setPos(self, x, y):
		self.pos_x = float(x)
		self.pos_y = float(y)
		return True
	def getPos(self):
		return (self.pos_x, self.pos_y)
	def setOwner(self, owner=None):
		self.owner = owner
	def getOwner(self):
		return self.owner
	def setVelocity(self, x, y):
		self.vel_x = float(x)
		self.vel_y = float(y)
	def getVelocity(self):
		return (self.vel_x, self.vel_y)
	def setHealth(self, health):
		self.health = health
	def getHealth(self):
		return self.health
	def setVisible(self, visible):
		self.visible = visible
	def getVisible(self):
		return self.visible