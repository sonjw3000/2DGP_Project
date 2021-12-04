from pico2d import *
import game_framework
import main_state

PIXEL_PER_METER = (10 / 0.2)  # 10 pixel 20 cm
BULLET_SPEED_KMPH = 40.0  # Km / Hour
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

BULLET_SPEED_Y_PPS = BULLET_SPEED_PPS


BULLET_SIZE = 20


class Bullet:
	image = None

	def __init__(self, x, y, b_dir):
		# It can active until x go + 500
		self.max_lifespan = 150
		self.cur_life = 0
		self.x, self.y = x, y

		self.bef_y = y

		self.x_Speed = -BULLET_SPEED_PPS + 2 * b_dir * BULLET_SPEED_PPS
		self.y_Speed = -BULLET_SPEED_Y_PPS / 2

		self.frame = 0

	def update(self):
		# Move here
		self.bef_y = self.y
		self.frame = (self.frame + 2) % 40

		self.cur_life += 1

		self.x += self.x_Speed * game_framework.frame_time
		self.y += self.y_Speed * game_framework.frame_time
		self.y_Speed -= 10 * BULLET_SPEED_Y_PPS * game_framework.frame_time

		if self.y_Speed < -BULLET_SPEED_Y_PPS:
			self.y_Speed = -BULLET_SPEED_Y_PPS

	# return true when it is alive
	def is_still_alive(self):
		return self.cur_life < self.max_lifespan

	def hit_floor(self):
		self.y_Speed = self.y_Speed * -1
		self.y = self.bef_y

	def get_position(self):
		return (self.x - BULLET_SIZE / 2,
				self.y - BULLET_SIZE / 2,
				self.x + BULLET_SIZE / 2,
				self.y + BULLET_SIZE / 2)

	def draw(self):
		# draw_rectangle(*(self.get_position()))
		self.image.clip_draw(9 * (self.frame // 10), 0, 9, 9,
							   self.x - main_state.screen_offset, self.y, BULLET_SIZE, BULLET_SIZE)
		pass

	@classmethod
	def set_image(cls, tileImage):
		cls.image = tileImage
