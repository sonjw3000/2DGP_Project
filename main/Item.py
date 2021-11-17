from pico2d import *
import Tile
import game_framework

ITEM_SIZE = Tile.TILE_SIZE

TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


# 0 : flower
# 1 : star
# 2 : coin
# 3 : mushroom(red, size + 1)
# 4 : mushroom(green, life + 1)

class Item:
	__image = None
	
	def __init__(self, x, y, item_type):
		self.__x, self.__y = x, y
		self.__type = item_type
		self.__frame = 0

		if Item.__image is None:
			__image = load_image("./resource/items.png")

	def update(self):
		# if type is sth:
		if self.__type == 1 or self.__type == 3 or self.__type == 4:
			# move to right dir
			pass

		if self.__type <= 3:
			self.__frame = (self.__frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

		pass

	def get_position(self):
		return (self.__x - Tile.TILE_SIZE / 2,
				self.__y - Tile.TILE_SIZE / 2,
				self.__x + Tile.TILE_SIZE / 2,
				self.__y + Tile.TILE_SIZE / 2)

	def draw(self):
		draw_rectangle(*(self.get_position()))

		Item.__image.clip_draw(9 * int(self.__frame), 0, 9, 9, self.__x, self.__y, ITEM_SIZE, ITEM_SIZE)
