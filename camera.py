from entity import Entity

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CHASECAM_MARGIN = 100
CHASECAM_VERT_MARGIN = 100
CHASECAM_IMPULSE = 7

class Camera(Entity):
	def __init__(self, display, scene=None, console=None, x=0, y=0, owner=None):
		Entity.__init__(self, owner, 0)
		self.display = display
		self.surface = display.getSurface()
		self.scene = scene
		self.console = console

	def respectBoundry(self):
		if self.pos_x < 0: self.pos_x = 0
		elif self.pos_x > 4096 - CAMERA_WIDTH: self.pos_x = 4096 - CAMERA_WIDTH
		if self.pos_y < 0: self.pos_y = 0
		elif self.pos_y > 4096: self.pos_y = 4096

	def move(self, frameDT):
		Entity.move(self, frameDT)
		if not self.owner: return

		owner_x = self.owner.pos_x * 10
		owner_y = self.owner.pos_y * 16
		#print owner_x, owner_y, self.pos_x, self.pos_y
		if owner_x + CHASECAM_MARGIN > self.pos_x + CAMERA_WIDTH:
			self.impulse(CHASECAM_IMPULSE)
		elif owner_x - CHASECAM_MARGIN < self.pos_x:
			self.impulse(-CHASECAM_IMPULSE)

		if owner_y + CHASECAM_VERT_MARGIN > self.pos_y + CAMERA_HEIGHT:
			self.impulse(0, CHASECAM_IMPULSE)
		elif owner_y - CHASECAM_VERT_MARGIN < self.pos_y:
			self.impulse(0, -CHASECAM_IMPULSE)

	def drawLayer(self, layer, frameDT):
		cur_x = self.pos_x / layer.sfactor_x
		cur_y = self.pos_y / layer.sfactor_y

		# Draw the tilemap first
		if layer.map:
			tx = int(cur_x / 64)
			ty = int(cur_y / 64)
			for y in range(0, 9):
				for x in range(0, 12):
					tile = layer.map[ty+y][tx+x]
					if tile.visible:
						dx = (x*tile.width) - (int(cur_x) & 63)
						dy = (y*tile.height) - (int(cur_y) & 63)
						tile.sprites[tile.sprite].draw(frameDT, self.surface, dx, dy)

		# Now draw the entities
		for ent in layer.entities:
			cx, cy = ent.getPos()
			if cx < cur_x or cx > cur_x + CAMERA_WIDTH: continue
			if cy < cur_y or cy > cur_y + CAMERA_WIDTH: continue
			ent.draw(frameDT, self.surface, int(cx - cur_x), int(cy - cur_y))

	def snap(self, frameDT):
		self.display.clear()
		for layer in reversed(self.scene.layers):
			self.drawLayer(layer, frameDT)
		self.console.draw(self.surface, frameDT, 0, 0)
		self.display.update()