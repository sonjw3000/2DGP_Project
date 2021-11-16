from pico2d import *

MONSTER_SPEED_X = 1.5
MONSTER_SIZE = 40


class Monster:
	__image = None

	def __init__(self, x, y, mon_type, b_dir):

		if Monster.__image == None:
			img = load_image("./resource/monsters.png")
			Monster.set_image(img)

		self.__x, self.__y = x, y
		self.__dir = b_dir

		self.__ySpeed = 0

		# type == 0 : turtle
		# type == 1 : gummba
		self.__type = mon_type
		self.__frame = 0

	def update(self, y_col=False):
		# Move here
		self.__x -= (1 - self.__dir * 2) * MONSTER_SPEED_X

		if not y_col:
			self.__y -= self.__ySpeed
			self.__ySpeed += 0.2
			if self.__ySpeed >= 2:
				self.__ySpeed = 2
		else:
			self.__ySpeed = 0
		self.__frame = (self.__frame + 2) % 20

	def get_position(self):
		return (self.__x - MONSTER_SIZE / 2,
				self.__y - MONSTER_SIZE / 2,
				self.__x + MONSTER_SIZE / 2,
				self.__y + MONSTER_SIZE / 2)

	def draw(self):
		self.__image.clip_draw(17 * (self.__frame // 10), self.__type * 23, 16, 16 + ((self.__type == 0) * 7),
							   self.__x, self.__y, MONSTER_SIZE, MONSTER_SIZE + ((self.__type == 0) * MONSTER_SIZE / 2))

	def reverse(self):
		self.__dir = not self.__dir
		self.__x -= (1 - self.__dir * 2) * MONSTER_SPEED_X

	@classmethod
	def set_image(cls, monster_image):
		cls.__image = monster_image
