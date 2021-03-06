from pico2d import *
import game_framework
import main_state

MONSTER_SPEED_X = 1.5
MONSTER_SIZE = 40

# Monster Run Speed
# Monster Speed 		: 20km/h
# Monster Size 			: 160 * 80
# Monster Pixel Size	: (TileSize * 2) * TileSize
PIXEL_PER_METER = (10 / 0.2)  # 10 pixel 20 cm
MONSTER_SPEED_KMPH = 5.0  # Km / Hour
MONSTER_SPEED_MPM = (MONSTER_SPEED_KMPH * 1000.0 / 60.0)
MONSTER_SPEED_MPS = (MONSTER_SPEED_MPM / 60.0)
MONSTER_SPEED_PPS = (MONSTER_SPEED_MPS * PIXEL_PER_METER)

MONSTER_TERMINAL_VELOCITY_KMPH = 80.0  # Km / Hour
MONSTER_TERMINAL_VELOCITY_MPM = (MONSTER_TERMINAL_VELOCITY_KMPH * 1000.0 / 60.0)
MONSTER_TERMINAL_VELOCITY_MPS = (MONSTER_TERMINAL_VELOCITY_MPM / 60.0)
MONSTER_TERMINAL_VELOCITY_PPS = (MONSTER_TERMINAL_VELOCITY_MPS * PIXEL_PER_METER)

# Running Action Speed
# 초당 50번 (0.02에 한번)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


class Monster:
	image = None

	def __init__(self, x, y, mon_type, b_dir):
		self.x, self.y = x, y
		self.dir = b_dir

		self.speed_y = 0

		self.speed_x = MONSTER_SPEED_PPS * 2
		self.bRun = False

		# type == 0 : turtle
		# type == 1 : gummba
		self.type = mon_type
		self.frame = 0
		self.bDead = False
		self.how = False
		self.lifetime = 0

	def update(self):
		# Move here
		# x axis
		self.lifetime += game_framework.frame_time * self.bDead

		self.x -= (1 - self.dir * 2) * MONSTER_SPEED_PPS * game_framework.frame_time * (not self.bDead)

		if self.bRun:
			self.x -= (1 - self.dir * 2) * MONSTER_SPEED_PPS * game_framework.frame_time

		# y axis
		self.speed_y -= 12 * PIXEL_PER_METER * game_framework.frame_time
		if (self.bDead and not self.how) and not self.bRun:
			self.speed_y = 0

		if self.speed_y < -MONSTER_TERMINAL_VELOCITY_PPS:
			self.speed_y = -MONSTER_TERMINAL_VELOCITY_PPS

		self.y += self.speed_y * game_framework.frame_time

		if self.bDead:
			self.frame = 2 + self.how
		else:
			self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) \
						 % FRAMES_PER_ACTION



	def get_position(self):
		return (self.x - MONSTER_SIZE / 2,
				self.y - MONSTER_SIZE / 2,
				self.x + MONSTER_SIZE / 2,
				self.y + MONSTER_SIZE / 2)

	# foot = false, bullet = true
	def go_dead(self, how):
		if self.bDead:
			self.bRun = not self.bRun
			if self.bRun:
				self.lifetime = 0
				self.speed_x = MONSTER_SPEED_PPS * 2
			return
		self.bDead = True
		self.bRun = False
		self.how = how and self.type != 0
		self.speed_y = 300 * how

	def go_live(self):
		self.bDead = False
		self.how = False
		self.bRun = False
		self.lifetime = 0

	def life_dead(self):

		if self.bRun:
			return False

		return (self.lifetime >= 1.25 + 1.75 * (self.type == 0))

	def draw(self):
		# draw_rectangle(*(self.get_position()))

		Monster.image.clip_draw(17 * int(self.frame) + 68 * (not self.dir), self.type * 23, 16, 16 + ((self.type == 0) * 7),
								  self.x - main_state.screen_offset, self.y,
								MONSTER_SIZE, MONSTER_SIZE)

	def reverse(self):
		self.dir = not self.dir
		self.x -= (1 - self.dir * 2) * MONSTER_SPEED_X

	def land(self, y_pos):
		self.speed_y = 0
		self.y = y_pos + MONSTER_SIZE / 2

	@classmethod
	def set_image(cls, monster_image):
		cls.image = monster_image

	# 저장할 정보를 선택하는 함수
	def __getstate__(self):
		# x, y, dir, type
		state = {'x': self.x, 'y': self.y, 'dir': self.dir, 'type': self.type}
		return state

	# 정보를 저장하는 함수
	def __setstate__(self, state):
		self.__init__(0, 60, 0, 0)
		self.__dict__.update(state)
