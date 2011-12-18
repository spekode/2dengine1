from display import Display
from camera import Camera
from player import Player
from scene import getScene
import sys
from text import TextConsole

def keyUnbound(key, state):
	print "Unbound key:", key, "State:", state

class Game(object):
	controlBinds = {
		'left':keyUnbound,
		'right':keyUnbound,
		'up':keyUnbound,
		'down':keyUnbound,
		'enter':keyUnbound,
		'pgdn':keyUnbound,
		'pgup':keyUnbound,
		'home':keyUnbound,
		'end':keyUnbound,
		'w':keyUnbound,
		'a':keyUnbound,
		's':keyUnbound,
		'd':keyUnbound
	}

	def __init__(self, level='level1'):
		self.level = level
		self.console = TextConsole()
		self.display = Display()
		self.scene = getScene(self.console)
		self.scene.player1 = Player()
		self.scene.player1.character.setColor((100, 255, 0))
		self.camera = Camera(self.display, self.scene, self.console)
		self.scene.add(self.camera, 0)


		# Default controls
		self.controlBinds['a'] = self.scene.player1.left
		self.controlBinds['d'] = self.scene.player1.right
		self.controlBinds['w'] = self.scene.player1.up
		self.controlBinds['s'] = self.scene.player1.down
		self.controlBinds['up'] = self.scene.player1.fireUp
		self.controlBinds['down'] = self.scene.player1.fireDown
		self.controlBinds['left'] = self.scene.player1.fireLeft
		self.controlBinds['right'] = self.scene.player1.fireRight
		#self.controlBinds['enter'] =
		#self.controlBinds['pgdn'] = self.camera.scrollDown
		#self.controlBinds['pgup'] = self.camera.scrollUp

		self.camera.setPos(0, 0)
		#self.camera.vel_x = 100.0
		self.camera.resistance_x = 400.0
		self.camera.resistance_y = 400.0
		#self.camera.setOwner(player1)
	
	def loadLevel(self, level):
		self.scene.loadLevel(self.level)

	def update(self, kdown, kup, other):
		for key in self.controlBinds:
			if key in kdown:
				self.controlBinds[key](key, True)
			if key in kup:
				self.controlBinds[key](key, False)
		
	def run(self, frameDT):
		# Run a frame

		# Check for 'dead' entities and let everyone think
		for layer in self.scene.layers:
			deadEnts = []
			for ent in layer.entities:
				if ent.health == -1:
					deadEnts.append(ent)
				else:
					ent.think(frameDT)
					ent.move(frameDT)
			for ent in deadEnts:		
				layer.entities.remove(ent)

		# Check for collisions
		for ent in self.scene.layers[3].entities:
			ex, ey = ent.getPos()
			# Check for collisions with the map
			if self.console.buffer[int(ey)][int(ex)] != ' ':
				ent.collide([(None, (int(ex), int(ey)))])
			else:
				ent.oldpos_x = ex
				ent.oldpos_y = ey
