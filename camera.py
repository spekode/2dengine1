from entity import Entity

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CHASECAM_MARGIN = 225
CHASECAM_VERT_MARGIN = 75

class Camera(Entity):
	def __init__(self, display, scene=None, x=0, y=0, owner=None):
		Entity.__init__(self, owner, 0)
		self.display = display
		self.scene = scene

	def constrainPosition(self):
		if self.pos_x < 0: self.pos_x = 0
		elif self.pos_x > 4096: self.pos_x = 4096
		if self.pos_y < 0: self.pos_y = 0
		elif self.pos_y > 4096: self.pos_y = 4096

	def move(self, frameDT):
		Entity.move(self, frameDT)
		if not self.owner: return

		if self.owner.pos_x + CHASECAM_MARGIN > self.pos_x + CAMERA_WIDTH:
			self.impulse(25)
		elif self.owner.pos_x - CHASECAM_MARGIN < self.pos_x:
			self.impulse(-25)

		if self.owner.pos_y + CHASECAM_VERT_MARGIN > self.pos_y + CAMERA_HEIGHT:
			self.impulse(0, 25)
		elif self.owner.pos_y - CHASECAM_VERT_MARGIN < self.pos_y:
			self.impulse(0, -25)

	def snap(self, frameDT):
		self.constrainPosition()
		self.display.clear()
		surface = self.display.getSurface()
		for layer in reversed(self.scene.layers):
			# Draw the tilemap first
			if layer.map:
				cur_x = self.pos_x / layer.sfactor_x
				cur_y = self.pos_y / layer.sfactor_y
				tx = int(cur_x / 64)
				ty = int(cur_y / 64)
				for y in range(0, 9):
					for x in range(0, 12):
						tile = layer.map[ty+y][tx+x]
						if tile.visible:
							dx = (x*tile.width) - (int(cur_x) & 63)
							#if layer.sfactor_x != 1: dx -= int(cur_x / layer.sfactor_x)
							dy = (y*tile.height) - (int(cur_y) & 63)
							#if layer.sfactor_y != 1: dy -= int(self.pos_y / layer.sfactor_y)
							tile.sprites[tile.sprite].draw(frameDT, surface, dx, dy)

			# Now draw the entities
			for ent in layer.entities:
				cx, cy = ent.getPos()
				ent.draw(frameDT, surface, cx - self.pos_x, cy - self.pos_y)
		self.display.update()