from pico2d import *
import Tile
import game_framework
import main_state
# Tile.TILE_SIZE

TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

ITEM_SIZE = 40

PIXEL_PER_METER = (10 / 0.2)  # 10 pixel 20 cm
ITEM_SPEED_KMPH = 5.0  # Km / Hour
ITEM_SPEED_MPM = (ITEM_SPEED_KMPH * 1000.0 / 60.0)
ITEM_SPEED_MPS = (ITEM_SPEED_MPM / 60.0)
ITEM_SPEED_PPS = (ITEM_SPEED_MPS * PIXEL_PER_METER)


ITEM_TERMINAL_VELOCITY_KMPH = 80.0  # Km / Hour
ITEM_TERMINAL_VELOCITY_MPM = (ITEM_TERMINAL_VELOCITY_KMPH * 1000.0 / 60.0)
ITEM_TERMINAL_VELOCITY_MPS = (ITEM_TERMINAL_VELOCITY_MPM / 60.0)
ITEM_TERMINAL_VELOCITY_PPS = (ITEM_TERMINAL_VELOCITY_MPS * PIXEL_PER_METER)

# 0 : flower
# 1 : star
# 2 : coin
# 3 : mushroom(red, size + 1)
# 4 : mushroom(green, life + 1)

class Item:
	image = None

	def __init__(self, x, y, item_type):
		self.x, self.y = x, y
		self.bef_x = x
		self.type = item_type
		self.frame = 0
		self.life_time = 0.0
		self.dir = 1
		self.speed_y = 0

		if self.type == 2:
			self.y -= ITEM_SIZE / 2

		if Item.image is None:
			Item.image = load_image("./resource/items.png")

	def update(self):
		self.bef_x = self.x
		# if type is sth:
		if self.type == 1 or self.type == 3 or self.type == 4:
			# move to right dir
			self.x += ITEM_SPEED_PPS * self.dir * game_framework.frame_time
			# y axis
			self.speed_y -= 12 * PIXEL_PER_METER * game_framework.frame_time
			if self.speed_y < -ITEM_TERMINAL_VELOCITY_PPS:
				self.speed_y = -ITEM_TERMINAL_VELOCITY_PPS

			self.y += self.speed_y * game_framework.frame_time

		elif self.type == 2:
			self.life_time += game_framework.frame_time
			self.y += ITEM_SIZE / 0.1 * game_framework.frame_time

		if self.type <= 2:
			self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

	def is_still_alive(self):
		# after 0.3 sec, erase effect
		return self.life_time < 0.1

	def get_position(self):
		return (self.x - Tile.TILE_SIZE / 2,
				self.y - Tile.TILE_SIZE / 2,
				self.x + Tile.TILE_SIZE / 2,
				self.y + Tile.TILE_SIZE / 2)

	def draw(self):
		# draw_rectangle(*(self.get_position()))

		Item.image.clip_draw(17 * int(self.frame),
							   17 * self.type, 16, 16,
							   self.x - main_state.screen_offset, self.y, ITEM_SIZE, ITEM_SIZE)

	def get_type(self):
		return self.type

	def reverse(self):
		self.dir = not self.dir
		# self.x -= (1 - self.dir * 2) * MONSTER_SPEED_X
		self.x = self.bef_x

	def land(self, y_pos):
		self.speed_y = 0
		self.y = y_pos + ITEM_SIZE / 2 + ((self.type == 0) * ITEM_SIZE / 2)
