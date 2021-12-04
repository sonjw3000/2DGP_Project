from pico2d import *
import Player
import Item
import game_framework
import main_state
import server
import GameWorld
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
	# imageSpriteOverWorld = load_image('./resource/tiles/overworld.png')
	imageSprite = None

	# right bottom == (0, 0)
	def __init__(self, x, y, collide, breakable, tile_number, item_num=0):
		self.x = x + TILE_SIZE // 2
		self.y = y + TILE_SIZE // 2

		self.offsetY = 0

		self.bCollideOn = collide
		self.__bBreakable = breakable
		self.type = tile_number

		self.bBreaking_Animation = False
		self.bBroken = False

		self.frame = 0
		# in items in here (in Item, -1)
		# 0 : None
		# 1 : flower
		# 2 : star
		# 3 : coin
		# 4 : mushroom(red, size + 1)
		# 5 : mushroom(green, life + 1)

		self.item = item_num

		# Types
		# Just see the image file, 0 == > (0,0) img, ...
		pass

	def get_position(self):
		return self.x - TILE_SIZE / 2, self.y - TILE_SIZE / 2, self.x + TILE_SIZE / 2, self.y + TILE_SIZE / 2

	def get_is_collidable(self, is_from_bottom=False):
		return self.bCollideOn or (is_from_bottom and self.item)

	def is_breakable(self):
		return self.__bBreakable

	def collide(self):
		if (self.type == 64 or self.item) and not self.bBroken:  # Item Box
			self.type = 64
			self.bCollideOn = True
			self.bBroken = True
			self.__bBreakable = False
			self.bBreaking_Animation = True
		elif self.type == 33:  # Breakable Block
			# self.type = 56
			self.bCollideOn = False
			self.bBreaking_Animation = True

	def update(self):
		# if col? then do sth
		if self.type == 64 and not self.bBroken:  # It's Item Box
			self.frame = \
				(self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
				FRAMES_PER_ACTION
		# self.frame = (self.frame + 1) % 40

		if self.bBreaking_Animation:
			# Blocks go up
			self.offsetY += game_framework.frame_time * 500

			# if complete going up
			if self.offsetY >= TILE_SIZE // 2:
				self.bBreaking_Animation = False
				# if type == 64: frame = 4 and go down
				if self.item:
					self.type = 64
					self.bBroken = True
					self.frame = 4

					# Make Item Here
					# if player is small, make mushroom
					item_type = self.item
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

					new_item = Item.Item(self.x, self.y + TILE_SIZE, item_type - 1)
					GameWorld.add_object(new_item, 1)
					server.items.append(new_item)
					pass
				elif self.type == 33:
					self.type = 56
					self.offsetY = 0
					# start fragment animation here
					pass

		pass

	# type 0 : over world, 1 : underground
	def draw(self):
		# draw_rectangle(*(self.get_position()))

		if self.bBreaking_Animation:
			self.imageSprite.clip_draw(
				1 + (56 % 16) * 17,
				1 + (56 // 16) * 17,
				16, 16, self.x - main_state.screen_offset, self.y, TILE_SIZE, TILE_SIZE)
			self.imageSprite.clip_draw(
				1 + (self.type % 16) * 17 + (int(self.frame)) * 17,
				1 + (self.type // 16) * 17,
				16, 16, self.x - main_state.screen_offset, self.y + self.offsetY, TILE_SIZE, TILE_SIZE)
		else:
			self.imageSprite.clip_draw(
				1 + (self.type % 16) * 17 + (int(self.frame)) * 17,
				1 + (self.type // 16) * 17,
				16, 16, self.x - main_state.screen_offset, self.y, TILE_SIZE, TILE_SIZE)

	def draw_breaking(self):
		if self.bBreaking_Animation:
			self.imageSprite.clip_draw(
				1 + (self.type % 16) * 17 + (int(self.frame)) * 17,
				1 + (self.type // 16) * 17,
				16, 16, self.x - main_state.screen_offset, self.y + self.offsetY, TILE_SIZE, TILE_SIZE)

	@classmethod
	def set_image(cls, tileImage):
		cls.imageSprite = tileImage

	# 저장할 정보를 선택하는 함수
	def __getstate__(self):
		# x, y, collide, breakable, tile_number, item_num=0
		state = {'x': self.x, 'y': self.y, 'bCollideOn': self.bCollideOn,
				 'type': self.type, 'item': self.item}
		return state

	# 정보를 저장하는 함수
	def __setstate__(self, state):
		self.__init__(0, 0, True, True, 0, 0)
		self.__dict__.update(state)


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
