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

	def __init__(self):
		self.console = TextConsole()
		self.display = Display()
		self.scene = getScene()
		self.camera = Camera(self.display, self.scene, self.console)
		
		self.level = 'terminal'

		player1 = Player()
		player1.setPos(1, 1)
		player1.setVisible(True)

		# Default controls
		self.controlBinds['a'] = player1.left
		self.controlBinds['d'] = player1.right
		self.controlBinds['w'] = player1.up
		self.controlBinds['s'] = player1.down
		self.controlBinds['up'] = player1.fireUp
		self.controlBinds['down'] = player1.fireDown
		self.controlBinds['left'] = player1.fireLeft
		self.controlBinds['right'] = player1.fireRight
		#self.controlBinds['enter'] =
		#self.controlBinds['pgdn'] = self.camera.scrollDown
		#self.controlBinds['pgup'] = self.camera.scrollUp

		self.scene.loadLevel(self.level)
		self.scene.add(self.camera, 0)
		self.scene.add(player1, 2)

		self.camera.setPos(0, 0)
		self.camera.vel_x = 100.0
		self.camera.resistance_x = 400.0
		self.camera.resistance_y = 400.0
		#self.camera.setOwner(player1)

		# Testing, testing..
		self.console.setChars("@", 21, 11)
		self.console.setColor((255,0,0), 21, 11)

	def update(self, kdown, kup, other):
		for key in self.controlBinds:
			if key in kdown:
				self.controlBinds[key](key, True)
			if key in kup:
				self.controlBinds[key](key, False)
		
	def run(self, frameDT):
		# Run a frame
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