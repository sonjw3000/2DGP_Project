import game_framework
import main_state
import GameWorld

FLAG_SIZE = 40


class Flag:
	image = None

	def __init__(self, x, y):
		self.bCaptured = False
		self.x, self.y = x, y

	def get_position(self):
		return (self.x - FLAG_SIZE / 2,
				self.y - FLAG_SIZE / 2,
				self.x + FLAG_SIZE / 2,
				self.y + FLAG_SIZE / 2)

	def update(self):
		pass


	@classmethod
	def set_image(cls, flag_image):
		cls.image = flag_image

	def draw(self):
		# draw_rectangle(*(self.get_position()))

		Flag.image.clip_draw(self.bCaptured * 50, 0, 50, 100,
							 self.x - main_state.screen_offset, self.y, FLAG_SIZE,
							 FLAG_SIZE * 2)

	def get_hit(self):
		self.bCaptured = True
		GameWorld.save(True)

	# 저장할 정보를 선택하는 함수
	def __getstate__(self):
		# x, y, dir, type
		state = {'x': self.x, 'y': self.y, 'bCaptured': self.bCaptured}
		return state

	# 정보를 저장하는 함수
	def __setstate__(self, state):
		self.__init__(0, 0)
		self.__dict__.update(state)

