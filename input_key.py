import pygame
from pygame.locals import *

keymap = {
	K_RETURN: 'enter',
	K_DOWN: 'down',
	K_UP: 'up',
	K_LEFT: 'left',
	K_RIGHT: 'right',
	K_PAGEDOWN: 'pgdn',
	K_PAGEUP: 'pgup',
	K_w: 'w',
	K_a: 'a',
	K_s: 's',
	K_d: 'd'
}

class KeyboardInput(object):
	def __init__(self):
		pass
	def retrieve(self):
		keys_pressed = []
		keys_released = []
		other = []
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key in keymap:
					keys_pressed.append(keymap[event.key])
			elif event.type == pygame.KEYUP:
				if event.key in keymap:
					keys_released.append(keymap[event.key])
			elif event.type == pygame.QUIT:
				other.append('QUIT')
		return (keys_pressed, keys_released, other)

