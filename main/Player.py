from pico2d import *
from keyboard import is_pressed
# from Tile import TILE_SIZE
import Tile
import game_framework

# import keyboard

# Player Run Speed
# Player Speed 		: 20km/h
# Player Size 		: 160 * 80
# Player Pixel Size	: (TileSize * 2) * TileSize
PIXEL_PER_METER = (10 / 0.2)  # 10 pixel 20 cm
PLAYER_SPEED_KMPH = 20.0  # Km / Hour
PLAYER_SPEED_MPM = (PLAYER_SPEED_KMPH * 1000.0 / 60.0)
PLAYER_SPEED_MPS = (PLAYER_SPEED_MPM / 60.0)
PLAYER_SPEED_PPS = (PLAYER_SPEED_MPS * PIXEL_PER_METER)

PLAYER_TERMINAL_VELOCITY_KMPH = 80.0  # Km / Hour
PLAYER_TERMINAL_VELOCITY_MPM = (PLAYER_TERMINAL_VELOCITY_KMPH * 1000.0 / 60.0)
PLAYER_TERMINAL_VELOCITY_MPS = (PLAYER_TERMINAL_VELOCITY_MPM / 60.0)
PLAYER_TERMINAL_VELOCITY_PPS = (PLAYER_TERMINAL_VELOCITY_MPS * PIXEL_PER_METER)

# Running Action Speed
# 초당 50번 (0.02에 한번)
TIME_PER_ACTION = 0.02
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

PLAYER_SPEED_X = 0.3
PLAYER_MAX_SPEED_X = 2.5

PLAYER_SPEED_Y = 0.2
PLAYER_MAX_SPEED_Y = 7
PLAYER_MAX_JUMP_HEIGHT = 100


class Player:
	def __init__(self, x=8, y=16, size=2):
		# Init Image Sprite
		self.__characterImageSprite = load_image('./resource/Mario_Real.png')

		# Mario Moving bool variables
		self.__bRunning = False
		self.__bBreak = False
		self.__bSitDown = False
		self.__bRunning = False
		self.__bAttack = False
		self.__bJump = False
		self.__bFalling = False

		# Set Pos
		self.__x = x
		self.__y = y

		# bef pos
		self.__bef_x = x
		self.__bef_y = y

		# Mario Current Size
		self.__size = size

		# Mario Move Direction -1 : left, 0 : Idle, 1 : Right
		self.__imgSprite = 0
		self.__frame = 0
		self.__bLookRight = True

		self.__speed_x = 0
		self.__speed_y = 0

		self.__dir = 0

		self.__yMove = 0

	# Constructor End

	# Returns rectangle tuple (Left, Bottom, Right, Top)
	def get_position(self):
		return (self.__x - Tile.TILE_SIZE / 2,
				self.__y - Tile.TILE_SIZE,
				self.__x + Tile.TILE_SIZE / 2,
				self.__y + Tile.TILE_SIZE - ((self.__bSitDown or self.__size == 0) * Tile.TILE_SIZE))

	def hit_ceil(self):
		if self.__speed_y <= 0:
			return False

		self.__speed_y *= -1
		self.__bFalling = True
		return True

	def input(self):
		self.__dir = 0
		bKeyPressed = False
		self.__bRunning = False

		# Move Start
		if is_pressed('left'):
			bKeyPressed = True
			self.__bRunning = True

			# Speed Setting
			self.__dir -= 1

			# Flag Setting
			if self.__speed_x > 0:
				# Breaking
				self.__speed_x -= PLAYER_SPEED_X / 2
				self.__bLookRight = False
				self.__bBreak = True
			else:
				# Running
				self.__bLookRight = False
				if self.__bBreak:
					if self.__speed_x <= -PLAYER_SPEED_X / 2:
						self.__bBreak = False

		if is_pressed('right'):
			bKeyPressed = True
			self.__bRunning = True

			# Speed Setting
			self.__dir += 1

			# Flag Setting
			if self.__speed_x < 0:
				# Breaking
				self.__speed_x += PLAYER_SPEED_X / 2
				self.__bLookRight = True
				self.__bBreak = True
			else:
				# Running
				self.__bLookRight = True
				if self.__bBreak:
					if self.__speed_x >= PLAYER_SPEED_X / 2:
						self.__bBreak = False

		if is_pressed('down'):
			bKeyPressed = True
			self.__bSitDown = True
		else:
			self.__bSitDown = False

		if is_pressed('up'):
			# jump gogo
			bKeyPressed = True
			if not self.__bFalling:
				self.__speed_y = PLAYER_TERMINAL_VELOCITY_PPS
				self.__bJump = True
				self.__yMove += self.__speed_y
			if self.__yMove >= PLAYER_MAX_JUMP_HEIGHT:
				self.__bFalling = True
		else:
			self.__bFalling = True

		# Slow Down
		if self.__speed_x > 0:
			self.__speed_x -= PLAYER_SPEED_X / 3
			if self.__speed_x < 0:
				self.__speed_x = 0

		elif self.__speed_x < 0:
			self.__speed_x += PLAYER_SPEED_X / 3
			if self.__speed_x > 0:
				self.__speed_x = 0

		if not bKeyPressed:
			self.__bBreak = False
		# Move End

		if self.__size == 2 and is_pressed('ctrl'):
			if not self.__bAttack:
				self.__bAttack = True
				# Make bullet here
				return self.__x + Tile.TILE_SIZE * (1 - 2 * (not self.__bLookRight)), self.__y
		else:
			self.__bAttack = False

		return None

	# Input End

	def go_x_back(self):
		self.__x = self.__bef_x

	def is_jumping(self):
		return self.__bJump or self.__bFalling

	def update(self):
		self.__bef_x = self.__x
		self.__bef_y = self.__y

		# x axis
		# accelerate, breaking
		if self.__dir > 0:
			self.__speed_x += PLAYER_SPEED_PPS * game_framework.frame_time * 2
			if self.__speed_x >= PLAYER_SPEED_PPS:
				self.__speed_x = PLAYER_SPEED_PPS
		elif self.__dir < 0:
			self.__speed_x -= PLAYER_SPEED_PPS * game_framework.frame_time * 2
			if self.__speed_x <= -PLAYER_SPEED_PPS:
				self.__speed_x = -PLAYER_SPEED_PPS
		else:
			if self.__speed_x > 0:
				self.__speed_x -= PLAYER_SPEED_PPS * game_framework.frame_time * 2
				if self.__speed_x < 0:
					self.__speed_x = 0
			elif self.__speed_x < 0:
				self.__speed_x += PLAYER_SPEED_PPS * game_framework.frame_time * 2
				if self.__speed_x > 0:
					self.__speed_x = 0
		self.__x += self.__speed_x * game_framework.frame_time

		# y axis
		self.__speed_y -= 9.8 * PIXEL_PER_METER * game_framework.frame_time
		if self.__speed_y > -PLAYER_TERMINAL_VELOCITY_PPS:
			self.__speed_y = -PLAYER_TERMINAL_VELOCITY_PPS

		# self.__y += self.__speed_y * game_framework.frame_time

		# # It's falling and land
		# if (self.__speed_y < 0 and self.__bFalling) and land:
		# 	self.__y = land + Tile.TILE_SIZE
		# 	self.__speed_y = 0
		# 	self.__bJump = False
		# 	self.__bFalling = False
		# 	self.__yMove = 0
		#
		# if not land and not self.__bJump:
		# 	self.__bFalling = True
		pass

	def draw(self):
		# print(self.__speed_x)
		# img start pos (0,1)
		# x offset : 17
		# y offset : 33
		# character size : 16 x 32, if size == 0: 16 x 16

		# Sprite 0 : Idle
		# Sprite 1 : Jump
		# Sprite 2 ~ 5 : Run
		# Sprite 6 : Attack(Size : 2), Empty(Size : 1), Dead(Size : 0)
		# Sprite 7 : Breaking
		# Sprite 8 : Sit Down

		# Set Img Sprite
		# if self.__speed_x == 0 and not self.__bBreak:
		# 	self.__imgSprite = 0

		bFrame = False

		# Image priority
		# (attack) > jump > sit > break > running > idle
		self.__imgSprite = 0
		if self.__bAttack:
			self.__imgSprite = 6
		elif self.__bJump or self.__bFalling:
			self.__imgSprite = 1
		elif self.__bSitDown:
			self.__imgSprite = 8
		elif self.__bBreak:
			self.__imgSprite = 7
		elif self.__bRunning:
			self.__imgSprite = 2
			bFrame = True

		draw_rectangle(*(self.get_position()))

		# Set Frame
		if bFrame:
			# self.__frame = (self.__frame + 1) % 40
			self.__frame = (self.__frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
		else:
			self.__frame = 0

		self.__characterImageSprite.clip_draw(
			(self.__imgSprite + (bFrame * self.__frame // 10)) * 17 + 153 * self.__bLookRight,
			(2 - self.__size) * 33,
			16, 32, self.__x, self.__y, Tile.TILE_SIZE, Tile.TILE_SIZE + (Tile.TILE_SIZE * (not self.__size == 0)))

	# Draw End

	# returns true when dir == right
	def get_dir(self):
		return self.__bLookRight

	# Test Funcs
	def sprite_up(self):
		self.__imgSprite += 1

	def sprite_down(self):
		self.__imgSprite -= 1

	def size_up(self):
		self.__size += 1

	def size_down(self):
		self.__size -= 1


# Test Funcs End


# Class End


# Mario Test
if __name__ == "__main__":
	open_canvas()

	bGameLoop = True
	mario = Player(20, 40)

	# Game Loop
	while bGameLoop:
		mario.input()

		events = get_events()
		for event in events:
			if event.type == SDL_QUIT:
				bGameLoop = False
			elif event.key == SDLK_F1:
				mario.sprite_up()
			elif event.key == SDLK_F2:
				mario.sprite_down()
			elif event.key == SDLK_F3:
				mario.size_up()
			elif event.key == SDLK_F4:
				mario.size_down()

		mario.move()
		delay(0.01)

		clear_canvas()
		mario.draw()
		update_canvas()
	close_canvas()
