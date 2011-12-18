import pygame

class Display(object):
	def __init__(self):
		#self.surface = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
		self.surface = pygame.display.set_mode((640, 480))
		self.surface.set_colorkey((0xDD, 0xEE, 0xFF), pygame.RLEACCEL)
	def clear(self):
		self.surface.fill((0,0,0))
	def update(self):
		pygame.display.flip()
	def getSurface(self):
		return self.surface