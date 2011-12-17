#!/usr/bin/python
import pygame
from pygame.locals import *
from timer import Timer
from game import Game
from input_key import KeyboardInput
import time

MaxFPS = 60.0
MaxFPSWait = 1000/MaxFPS

gameTime = Timer()
frameDT = 0.0


def engineInit():
	global display, game, keyInput, scene, camera
	pygame.init()

	keyInput = KeyboardInput()
	game = Game()

	levelInit('terminal')

def levelInit(game_level):
	pass

def gameLoop():
	global frameDT
	frameTime = Timer()
	frameDT = 0.0
	while 1:
		frameTime.start()

		# INPUT
		keys_down, keys_up, other = keyInput.retrieve()

		# UPDATE
		result = game.update(keys_down, keys_up, other)

		# LOGIC
		result = game.run(frameDT)

		# RENDER
		game.camera.snap(frameDT)

		# WAIT
		endFrameTime = frameTime.elapsed()
		if endFrameTime < MaxFPSWait: time.sleep((MaxFPSWait - endFrameTime) / 1000)
		
		frameDT = frameTime.elapsed()

def main():
	engineInit()
	while 1:
		levelInit(game.level)
		while 1:
			gameTime.start()
			gameLoop()

if __name__ == '__main__':
	main()