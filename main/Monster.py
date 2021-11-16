from pico2d import *
import game_framework

MONSTER_SPEED_X = 1.5
MONSTER_SIZE = 40

# Monster Run Speed
# Monster Speed 		: 20km/h
# Monster Size 			: 160 * 80
# Monster Pixel Size	: (TileSize * 2) * TileSize
PIXEL_PER_METER = (10 / 0.2)  # 10 pixel 20 cm
Monster_SPEED_KMPH = 5.0  # Km / Hour
Monster_SPEED_MPM = (Monster_SPEED_KMPH * 1000.0 / 60.0)
Monster_SPEED_MPS = (Monster_SPEED_MPM / 60.0)
Monster_SPEED_PPS = (Monster_SPEED_MPS * PIXEL_PER_METER)


# Running Action Speed
# 초당 50번 (0.02에 한번)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


class Monster:
	__image = None

	def __init__(self, x, y, mon_type, b_dir):
		self.__x, self.__y = x, y
		self.__dir = b_dir

		self.__ySpeed = 0

		# type == 0 : turtle
		# type == 1 : gummba
		self.__type = mon_type
		self.__frame = 0

	def update(self):
		# Move here
		self.__x -= (1 - self.__dir * 2) * Monster_SPEED_PPS * game_framework.frame_time
		# if not y_col:
		# 	self.__y -= self.__ySpeed
		# 	self.__ySpeed += 0.2
		# 	if self.__ySpeed >= 2:
		# 		self.__ySpeed = 2
		# else:
		# 	self.__ySpeed = 0
		self.__frame = (self.__frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

	def get_position(self):
		return (self.__x - MONSTER_SIZE / 2,
				self.__y - MONSTER_SIZE / 2,
				self.__x + MONSTER_SIZE / 2,
				self.__y + MONSTER_SIZE / 2)

	def draw(self):
		draw_rectangle(*(self.get_position()))

		Monster.__image.clip_draw(17 * int(self.__frame), self.__type * 23, 16, 16 + ((self.__type == 0) * 7),
								  self.__x, self.__y, MONSTER_SIZE,
								  MONSTER_SIZE + ((self.__type == 0) * MONSTER_SIZE / 2))

	def reverse(self):
		self.__dir = not self.__dir
		self.__x -= (1 - self.__dir * 2) * MONSTER_SPEED_X

	@classmethod
	def set_image(cls, monster_image):
		cls.__image = monster_image
