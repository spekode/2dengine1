from display import Display
from camera import Camera
from player import Player
from scene import getScene
import sys
from text import TextConsole
from common import *

MAXIMUM_COLLISION_RANGE = 10

def collisionTimeCheck(ent1, ent2, vel1, vel2, stime, etime, step):
	entA = Vec2(0,0) + ent1
	entB = Vec2(0,0) + ent2
	while stime < etime:
		ent1 = entA + (vel1 * stime)
		ent2 = entB + (vel2 * stime)
		distance = abs((ent1 - ent2).mag)
		if distance < 0.75:
			#print "COLLISION BETWEEN FRAMES ", stime, ent1, ent2, distance
			#while True: pass
			return (ent2, (ent1.x, ent1.y))
		stime += step
	return None

def collisionCheckMapEnt(ent):
	pass

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
		self.console.setChars("\x7f", 28, 10)

	def update(self, kdown, kup, other):
		for key in self.controlBinds:
			if key in kdown:
				self.controlBinds[key](key, True)
			if key in kup:
				self.controlBinds[key](key, False)

	def collisionEntityCheck(self, ent, layer):
		global frameDTfract
		ev = Vec2(ent.pos_x, ent.pos_y)
		collisionList = []
		for cent in layer.entities:
			if cent == ent:
				continue

			# Straight forward check, are we too close?
			cev = Vec2(cent.pos_x, cent.pos_y)
			distance = abs((ev - cev).mag)
			if distance < 1: collisionList.append((cent, (0,0)))
			elif distance > MAXIMUM_COLLISION_RANGE: continue
			else:
				# We aren't too close /now/, but did we collide between frames?
				old_ev = Vec2(ent.oldpos_x, ent.oldpos_y)
				ev_vel = Vec2(ent.vel_x, ent.vel_y)
				old_cev = Vec2(cent.oldpos_x, cent.oldpos_y)
				cev_vel = Vec2(cent.vel_x, cent.vel_y)
				cevent = collisionTimeCheck(old_ev, old_cev, ev_vel, cev_vel, 0.001, frameDTfract, 0.002)
				if cevent:
					collisionList.append(cevent)

		return collisionList

	def collisionLayerCheck(self, layer):
		for ent in layer.entities:
			if ent.health <= 0: continue # don't collision-check the dead
			ex, ey = ent.getPos()
			collisionList = []

			# Check for collisions with the map
			if self.console.buffer[int(ey)][int(ex)] != ' ':
				collisionList.append((None, (int(ex), int(ey))))

			# Check for collisions with other ents
			for clayer in self.scene.layers:
				collisionList += self.collisionEntityCheck(ent, clayer)

			# Tell the ent about them
			if len(collisionList):
				ent.collide(collisionList)

	def run(self, frameDT):
		# Run a frame
		global frameDTfract
		frameDTfract = frameDT/1000

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
				zombie = layer.entities.remove(ent)
				del zombie

		# Check for collisions
		for layer in self.scene.layers:
			self.collisionLayerCheck(layer)