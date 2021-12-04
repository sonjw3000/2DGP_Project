from pico2d import *
import Player
import Item
import game_framework
import main_state
import server

# Tile is square
TILE_SIZE = 40


# Floor : 0
# Normal Block : 33
# Empty_Sky = 56
# Item Block : 64

# 1 cycle : 1.6 sec
# 1 cycle = 4 frame
# 0.4sec + 1 frame
# ? Block
TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Tile:
	# __imageSpriteOverWorld = load_image('./resource/tiles/overworld.png')
	__imageSprite = None

	# right bottom == (0, 0)
	def __init__(self, x, y, collide, breakable, tile_number, item_num=0):
		self.__x = x + TILE_SIZE // 2
		self.__y = y + TILE_SIZE // 2

		self.__offsetY = 0

		self.__bCollideOn = collide
		self.__bBreakable = breakable
		self.__type = tile_number

		self.__bBreaking_Animation = False
		self.__bBroken = False

		self.__frame = 0
		# in items in here (in Item, -1)
		# 0 : None
		# 1 : flower
		# 2 : star
		# 3 : coin
		# 4 : mushroom(red, size + 1)
		# 5 : mushroom(green, life + 1)

		self.__item = item_num

		# Types
		# Just see the image file, 0 == > (0,0) img, ...
		pass

	def get_position(self):
		return self.__x - TILE_SIZE / 2, self.__y - TILE_SIZE / 2, self.__x + TILE_SIZE / 2, self.__y + TILE_SIZE / 2

	def get_is_collidable(self, is_from_bottom=False):
		return self.__bCollideOn or (is_from_bottom and self.__item)

	def is_breakable(self):
		return self.__bBreakable

	def collide(self):
		if (self.__type == 64 or self.__item) and not self.__bBroken:  # Item Box
			self.__type = 64
			self.__bCollideOn = True
			self.__bBroken = True
			self.__bBreakable = False
			self.__bBreaking_Animation = True
		elif self.__type == 33:  # Breakable Block
			# self.__type = 56
			self.__bCollideOn = False
			self.__bBreaking_Animation = True

	def update(self):
		# if col? then do sth
		if self.__type == 64 and not self.__bBroken:  # It's Item Box
			self.__frame = \
				(self.__frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
				FRAMES_PER_ACTION
			# self.__frame = (self.__frame + 1) % 40

		if self.__bBreaking_Animation:
			# Blocks go up
			self.__offsetY += game_framework.frame_time * 500

			# if complete going up
			if self.__offsetY >= TILE_SIZE // 2:
				self.__bBreaking_Animation = False
				# if type == 64: frame = 4 and go down
				if self.__item:
					self.__type = 64
					self.__bBroken = True
					self.__frame = 4

					# Make Item Here
					# if player is small, make mushroom
					item_type = self.__item
					if item_type == 1 or item_type == 4:
						if server.gamePlayer.get_size() >= 1:
							# flower
							item_type = 1
						else:
							# mushroom
							item_type = 4

					# coin earned, score + 100
					if item_type == 3:
						main_state.game_score += 100
						main_state.game_coin += 1

					new_item = Item.Item(self.__x, self.__y + TILE_SIZE, item_type - 1)
					main_state.game_objects.add_object(new_item, 1)
					server.items.append(new_item)
					pass
				elif self.__type == 33:
					self.__type = 56
					self.__offsetY = 0
					# start fragment animation here
					pass

		pass

	# type 0 : over world, 1 : underground
	def draw(self):
		# draw_rectangle(*(self.get_position()))

		if self.__bBreaking_Animation:
			self.__imageSprite.clip_draw(
				1 + (56 % 16) * 17,
				1 + (56 // 16) * 17,
				16, 16, self.__x - main_state.screen_offset, self.__y, TILE_SIZE, TILE_SIZE)
			self.__imageSprite.clip_draw(
				1 + (self.__type % 16) * 17 + (int(self.__frame)) * 17,
				1 + (self.__type // 16) * 17,
				16, 16, self.__x - main_state.screen_offset, self.__y + self.__offsetY, TILE_SIZE, TILE_SIZE)
		else:
			self.__imageSprite.clip_draw(
				1 + (self.__type % 16) * 17 + (int(self.__frame)) * 17,
				1 + (self.__type // 16) * 17,
				16, 16, self.__x - main_state.screen_offset, self.__y, TILE_SIZE, TILE_SIZE)

	def draw_breaking(self):
		if self.__bBreaking_Animation:
			self.__imageSprite.clip_draw(
				1 + (self.__type % 16) * 17 + (int(self.__frame)) * 17,
				1 + (self.__type // 16) * 17,
				16, 16, self.__x - main_state.screen_offset, self.__y + self.__offsetY, TILE_SIZE, TILE_SIZE)

	@classmethod
	def set_image(cls, tileImage):
		cls.__imageSprite = tileImage


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
