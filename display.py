import pygame

class Display(object):
	def __init__(self):
		#self.surface = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
		#self.surface = pygame.display.set_mode((640, 480), pygame.RLEACCEL)
		self.surface = pygame.display.set_mode((640, 480))
	def clear(self):
		self.surface.fill((0,0,0))
	def update(self):
		pygame.display.flip()
	def getSurface(self):
		return self.surface