from pico2d import *
import Player

# Tile is square
TILE_SIZE = 40


# Floor : 0
# Breakable Block : 33
# Empty_Sky = 56
# Item Block :


class Tile:
	# __imageSpriteOverWorld = load_image('./resource/tiles/overworld.png')
	__imageSpriteOverWorld = None

	# right bottom == (0, 0)
	def __init__(self, x, y, collide, breakable, tile_number, item_num=0):
		self.__x = x + TILE_SIZE // 2
		self.__y = y + TILE_SIZE // 2

		self.__bCollideOn = collide
		self.__bBreakable = breakable
		self.__type = tile_number

		self.__bBroken = False

		self.__frame = 0

		# Mushroom : 0
		# Flower : 1
		# Star : 2
		if self.__type == 64:
			self.__item = item_num

		# Types
		# Just see the image file, 0 == > (0,0) img, ...
		pass

	def get_position(self):
		return self.__x - TILE_SIZE / 2, self.__y - TILE_SIZE / 2, self.__x + TILE_SIZE / 2, self.__y + TILE_SIZE / 2

	def get_is_collidable(self):
		return self.__bCollideOn

	def is_breakable(self):
		return self.__bBreakable

	def update(self, collide=False):
		# if col? then do sth
		if collide:
			if self.__type == 64:  # Item Box
				self.__bBroken = True
				self.__bBreakable = False
				self.__frame = 4
			elif self.__type == 33:  # Breakable Block
				self.__type = 56

		if self.__type == 64 and not self.__bBroken:  # It's Item Box
			self.__frame = (self.__frame + 1) % 40
		pass

	# type 0 : over world, 1 : underground
	def draw(self):
		self.__imageSpriteOverWorld.clip_draw(
			1 + (self.__type % 16) * 17 + (self.__frame // 10) * 17,
			1 + (self.__type // 16) * 17,
			16, 16, self.__x, self.__y, TILE_SIZE, TILE_SIZE)

	@classmethod
	def set_image(cls, tileImage):
		cls.__imageSpriteOverWorld = tileImage


# Class End
#

if __name__ == "__main__":
	# Init game Settings
	open_canvas()

	tileImage = load_image('./resource/tiles/overworld.png')
	Tile.set_image(tileImage)

	gLoop = True
	mario = Player.Player(80, 80, 2)

	myTiles = [
		Tile(TILE_SIZE * 0, TILE_SIZE * 0, True, False, 0),
		Tile(TILE_SIZE * 1, TILE_SIZE * 0, True, False, 0),
		Tile(TILE_SIZE * 2, TILE_SIZE * 0, True, False, 0),
		Tile(TILE_SIZE * 3, TILE_SIZE * 0, True, False, 0),

		Tile(TILE_SIZE * 0, TILE_SIZE * 4, True, True, 33),
		Tile(TILE_SIZE * 1, TILE_SIZE * 4, True, True, 33),
		Tile(TILE_SIZE * 2, TILE_SIZE * 4, True, True, 33),
		Tile(TILE_SIZE * 3, TILE_SIZE * 4, True, True, 33),

		Tile(TILE_SIZE * 0, TILE_SIZE * 6, True, False, 64),
		Tile(TILE_SIZE * 1, TILE_SIZE * 6, True, False, 64),
		Tile(TILE_SIZE * 2, TILE_SIZE * 6, True, False, 64),
		Tile(TILE_SIZE * 3, TILE_SIZE * 6, True, False, 64),

		Tile(TILE_SIZE * 0, TILE_SIZE * 8, True, True, 33),
		Tile(TILE_SIZE * 1, TILE_SIZE * 8, True, True, 33),
		Tile(TILE_SIZE * 2, TILE_SIZE * 8, True, True, 33),
		Tile(TILE_SIZE * 3, TILE_SIZE * 8, True, True, 33),
	]

	# Game Loop
	while gLoop:
		events = get_events()
		for event in events:
			if event.type == SDL_QUIT:
				gLoop = False
		mario.input()

		for tile in myTiles:
			tile.update()
		mario.move()

		clear_canvas()
		mario.draw()
		for tile in myTiles:
			tile.draw()
		update_canvas()
		delay(0.01)

	close_canvas()
