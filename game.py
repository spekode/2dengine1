from display import Display
from camera import Camera
from player import Player
from scene import Scene
import sys

class Game(object):
	controlBinds = {
		'left':None,
		'right':None,
		'up':None,
		'down':None,
		'enter':None,
		'pgdn':None,
		'pgup':None,
		'home':None,
		'end':None
	}

	def __init__(self):
		self.display = Display()
		self.scene = Scene()
		self.camera = Camera(self.display, self.scene)
		
		self.level = 'intro'

		player1 = Player()
		player1.setPos(100, 100)
		player1.setVisible(True)

		# Default controls
		self.controlBinds['left'] = player1.left
		self.controlBinds['right'] = player1.right
		self.controlBinds['up'] = player1.up
		self.controlBinds['down'] = player1.down
		self.controlBinds['enter'] = sys.exit
		#self.controlBinds['pgdn'] = self.camera.scrollDown
		#self.controlBinds['pgup'] = self.camera.scrollUp

		self.scene.loadLevel(self.level)
		self.scene.add(self.camera, 0)
		self.scene.add(player1, 2)

		self.camera.setPos(0, 0)
		self.camera.vel_x = 100.0
		self.camera.resistance_x = 400.0
		self.camera.resistance_y = 400.0
		self.camera.setOwner(player1)

	def update(self, kdown, kup, other):
		for key in self.controlBinds:
			if key in kdown:
				self.controlBinds[key](True)
				print key
			if key in kup:
				self.controlBinds[key](False)
		
	def run(self, frameDT):
		# Run a frame
		for layer in self.scene.layers:
			for ent in layer.entities:
				ent.move(frameDT)