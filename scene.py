import sprite
import os

class Tile(object):
	def __init__(self, sprite=None, sprites=None):
		self.width = 64
		self.height = 64
		self.sprites = sprites
		self.sprite = sprite
		self.colRect = None

		self.collision = False
		self.visible = False

	def collide(self, entity):
		pass

class Layer(object):
	def __init__(self, mapdata=None, width=4096, height=4096):
		self.width = width
		self.height = height
		self.entities = []
		self.map = mapdata
		self.sfactor_x = 1
		self.sfactor_y = 1

	def setMapData(self, mapdata):
		self.map = mapdata
	def setSfactor(self, x=None, y=None):
		if x: self.sfactor_x = x
		if y: self.sfactor_y = y

class Scene(object):
	def __init__(self):
		self.layerCount = 8
		self.layers = [Layer()]
		self.tiles = []

	def loadTiles(self, tilelist):
		sprites = []
		for tile in tilelist:
			tmp = sprite.spriteLoad('./tiles/' + tile + '.png')
			sprites.append(Tile(tile, tmp))
		return sprites

	def loadLayer(self, level, layernum):
		mapdata = []
		try:
			for line in open("./levels/" + level + "/map" + str(layernum) + ".map"):
				mapdata.append([Tile(self.tiles[int(num)].sprite, self.tiles[int(num)].sprites) for num in line.split()])
		except: mapdata = None
		if mapdata:
			print mapdata[0]
			for row in mapdata:
				for tile in row:
					if tile.sprite != "notile": tile.visible = True
		layer = Layer(mapdata)
		try:
			lines = open("./levels/" + level + "/map" + str(layernum) + ".info").read().splitlines()
			print "###########3333##############"
			print "###########3333##############"
			print "###########3333##############"
			print "###########3333##############"
			print "###########3333##############"
			print "sfacts", int(lines[0].strip()), int(lines[1].strip())
			layer.setSfactor(int(lines[0].strip()), int(lines[1].strip()))
		except:
			pass

		return layer

	def loadLevel(self, level='intro'):
		# Get the tileset
		tilenames = []
		maptiles = open('./levels/' + level + '/tiles')
		for line in maptiles:
			tilenames.append(line.strip())
		self.tiles = self.loadTiles(tilenames)
		print self.tiles

		# Get the layers
		self.layers = []
		for i in range(0, self.layerCount):
			self.layers.append(self.loadLayer(level, i))
			print "layer", i, ":", self.layers[i]

	def add(self, ent, layer=0):
		self.layers[layer].entities.append(ent)