from text import TextCharacter

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
		self.oldpos_x = 0.0
		self.oldpos_y = 0.0
		self.pos_x = 0.0
		self.pos_y = 0.0
		self.vel_x = 0.0
		self.vel_y = 0.0
		self.constaccel_x = 0.0
		self.constaccel_y = 0.0
		self.resistance_x = 27.0
		self.resistance_y = 27.0
		self.rotation = 0.0
		
		self.colRect = None
		self.colCircle = ((0.0, 0.0), 0.5)

		self.health = 100
		self.visible = False

		self.touching = []

	# Actions (most likely overriden by a subclass)
	def think(self, frameDT): pass

	def accel(self, x, y, tlen=None, tfunc=LinearChange):
		self.accel_x += x
		self.accel_y += y

	def impulse(self, x=0, y=0):
		self.vel_x += x
		self.vel_y += y
	def collideHandler(self):
		for partner in self.touching:
			if partner[0] != None: pass
				#print "Entity on Entity collision"
			else:
				#print "Entity on Wall collision"
				ex, ey = self.getPos()
				wx, wy = partner[1]
				#ex = int(ex)
				#ey = int(ey)
				#wx = int(wx)
				#wy = int(wy)
				#print ex, ey, wx, wy, self.vel_x, self.vel_y
				self.pos_x = self.oldpos_x
				self.pos_y = self.oldpos_y
		self.touching = []

	def collide(self, partners=[]):
		self.touching += partners

	def death(self, attacker=None, deathtype=None): pass

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
			elif self.vel_y < -self.vel_y_max: self.vel_y = -self.vel_y_max	
		
		# Save position
		self.oldpos_x = self.pos_x
		self.oldpos_y = self.pos_y
		# Update position
		self.pos_x += self.vel_x * frameDTfract
		self.pos_y += self.vel_y * frameDTfract

		# Contain entity within an area (default is playfield)
		self.respectBoundry()

	def respectBoundry(self):
		if self.pos_y < 0: self.pos_y = 0
		elif self.pos_y > 29: self.pos_y = 29
		if self.pos_x < 0: self.pos_x = 0
		elif self.pos_x > 63: self.pos_x = 63

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
	def setOldPos(self, oldx, oldy):
		self.oldpos_x = oldx
		self.oldpos_y = oldy
		return True
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

class TextEntity(Entity):
	def __init__(self, owner=None, layer=None, char='@'):
		Entity.__init__(self, owner, layer)
		self.character = TextCharacter()
		self.character.setChar(char)

	def draw(self, frameDT, surface, x, y):
		if self.visible:
			cx = 10 * int(x)
			cy = 16 * int(y)

			self.character.draw(surface, frameDT, cx, cy)
	def getChar(self):
		return self.character.getChar()