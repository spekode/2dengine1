import pygame
from pygame.locals import *
import random

class TextConsole(object):
	def __init__(self):
		self.rows = 30
		self.cols = 64
		self.buffer = [[' ' for x in range(0, self.cols)] for i in range(0, self.rows)]
		self.bufferColors = [[(255,255,255) for x in range(0, self.cols)] for i in range(0, self.rows)]
		self.bufferColors[20][63] = (255,0,0)
		self.font = pygame.font.Font('fonts/mode7.ttf', 16)
		self.linesurfs = [[None, True] for x in range(0, self.rows)]

		self.textsurf = None

	def renderRow(self, rowindex):
		print "rendering row", rowindex
		linesurf = pygame.Surface((640, 16), pygame.RLEACCEL)
		linesurf.set_colorkey(0xDDEEFF, pygame.RLEACCEL)
		for i, col in enumerate(self.buffer[rowindex]):
			colsurf = self.font.render(col, 0, self.bufferColors[rowindex][i], (0xDD, 0xEE, 0xFF)).convert_alpha()
			colsurf.set_colorkey(0xDDEEFF, pygame.RLEACCEL)
			linesurf.blit(colsurf, ((i*10), 0))
		return linesurf

	def draw(self, surface, frameDT, x, y):
		for i, row in enumerate(self.buffer):
			if self.linesurfs[i][1] == True:
				self.linesurfs[i][0] = self.renderRow(i)
				self.linesurfs[i][1] = False
			textpos = self.linesurfs[i][0].get_rect().move(0, 16 * i)
			surface.blit(self.linesurfs[i][0], textpos)
	
	def setChars(self, chars, row, col):
		x = col
		self.linesurfs[row][1] = True # make surface dirty
		for char in chars:
			self.buffer[row][x] = char
			x += 1
	def setColor(self, color, row, col, len=1):
		self.linesurfs[row][1] = True
		for i in range(col, col+len):
			self.bufferColors[row][i] = color