import pygame
from pygame.locals import *

def spriteLoad(filename):
	""" Returns a sprite object """
	spriteinfo = {}
	sprites = {}
	surface = pygame.image.load(filename).convert()
	surface.set_colorkey(0xDDEEFF, pygame.RLEACCEL)
	for line in open(filename + ".sprite"):
		temp = line.strip().split()
		# dogman_jump 4 0 0 10 20 0.5
		spriteinfo[temp[0]] = { 'frames':int(temp[1]), 'x':int(temp[2]), 'y':int(temp[3]), 'width':int(temp[4]), 'height':int(temp[5]), 'fps':float(temp[6]) }
	for name in spriteinfo:
		sprites[name] = Sprite(name, surface, spriteinfo[name])
	return sprites

class Sprite(object):
	def __init__(self, name, spriteimage, spriteinfo):
		self.name = name
		self.image = spriteimage
		self.framenum = 0.0

		self.width = spriteinfo['width']
		self.height = spriteinfo['height']
		self.fps = spriteinfo['fps']
		self.fpsDT = 1000/self.fps
		self.frames = spriteinfo['frames']
		self.startx = spriteinfo['x']
		self.starty = spriteinfo['y']

	def reset(self):
		self.framenum = 0.0

	def frame(self, frameDT):
		""" Return the surface containing the current frame of the sprite and the rect to blit it """
		if self.frames == 1:
			frame = 0
		else:
			self.framenum += frameDT/self.fpsDT
			frame = int(self.framenum)
			if frame >= self.frames:
				self.framenum = 0
				frame = 0

		rect = pygame.Rect(self.startx + (frame * self.width), self.starty, self.width, self.height)

		return (self.image, rect)

	def draw(self, frameDT, surface, x, y):
		(frame, rect) = self.frame(frameDT)
		surface.blit(frame, (x - (self.width/2), y - (self.height/2)), area=rect)

if __name__ == '__main__':
	import time
	pygame.init()
#	surface = pygame.display.set_mode((640,480), pygame.FULLSCREEN)
	surface = pygame.display.set_mode((640,480))
	# Test
	loader = SpriteLoader()
	dork = loader.load("sprites/dork.png")

	for i in range(0,100):
		surface.fill((0,0,0))
		frameDT = 50.0
		dork['dork_idle'].draw(surface, 5,10)
		dork['dork_idle_slowmo'].draw(surface, 20,30)
		pygame.display.flip()
		time.sleep(0.05)