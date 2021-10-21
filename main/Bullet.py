from pico2d import *

BULLET_SPEED_X = 7
BULLET_SPEED_Y = 2.6

BULLET_SIZE = 20


class Bullet:
	__image = None

	def __init__(self, x, y, b_dir):
		# It can active until x go + 500
		self.__max_lifespan = 150
		self.__cur_life = 0
		self.__x, self.__y = x, y

		self.__x_Speed = -BULLET_SPEED_X + 2 * b_dir * BULLET_SPEED_X
		self.__y_Speed = -BULLET_SPEED_Y

		self.__frame = 0

	def update(self, y_col=False):
		# Move here
		self.__frame = (self.__frame + 2) % 40

		self.__cur_life += 1

		if y_col:
			self.__y_Speed *= -1
		if self.__y_Speed <= -BULLET_SPEED_Y:
			self.__y_Speed = -BULLET_SPEED_Y

		self.__x += self.__x_Speed
		self.__y += self.__y_Speed
		self.__y_Speed -= 0.2

		# return true when it is alive
		return self.__cur_life < self.__max_lifespan

	def get_position(self):
		return (self.__x - BULLET_SIZE / 2,
				self.__y - BULLET_SIZE / 2,
				self.__x + BULLET_SIZE / 2,
				self.__y + BULLET_SIZE / 2)

	def draw(self):
		self.__image.clip_draw(9 * (self.__frame // 10), 0, 9, 9, self.__x, self.__y, BULLET_SIZE, BULLET_SIZE)
		pass

	@classmethod
	def set_image(cls, tileImage):
		cls.__image = tileImage
