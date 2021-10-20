from pico2d import *


class Bullet:
	__image = None

	def __init__(self, x, y):
		# It can active until x go + 500
		self.__max_lifespan = 500
		self.__cur_life = 0
		self.__x, self.__y = x, y
		self.__frame = 0

	def update(self):
		# Move here
		self.__frame = (self.__frame + 1) % 40
		self.__x += 1

		return self.__cur_life >= self.__max_lifespan

	def draw(self):
		self.__image.clip_draw(9 * (self.__frame // 10),  0, 9, 9, self.__x, self.__y, 20, 20)
		pass

	def test_fucn(self):
		pass

	@classmethod
	def set_image(cls, tileImage):
		cls.__image = tileImage
