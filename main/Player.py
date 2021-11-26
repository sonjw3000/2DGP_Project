from pico2d import *
from keyboard import is_pressed
# from Tile import TILE_SIZE
import Tile
import Bullet
import game_framework
import GameWorld
import main_state

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

PLAYER_TERMINAL_VELOCITY_KMPH = 40.0  # Km / Hour
PLAYER_TERMINAL_VELOCITY_MPM = (PLAYER_TERMINAL_VELOCITY_KMPH * 1000.0 / 60.0)
PLAYER_TERMINAL_VELOCITY_MPS = (PLAYER_TERMINAL_VELOCITY_MPM / 60.0)
PLAYER_TERMINAL_VELOCITY_PPS = (PLAYER_TERMINAL_VELOCITY_MPS * PIXEL_PER_METER)

# Running Action Speed
# 0.5에 한번
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

PLAYER_MAX_JUMP_HEIGHT = 100  # pixel


class MovingState:
	# normal state
	pass


class HitState:
	pass


class DeadState:
	# boy's y speed += 40 and show dead
	pass


class EndState:
	# get down to the floor and move right 3 tiles
	pass


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

		# invincible control variables
		self.__bInvincible = False
		self.__invincible_timer = 0.0

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
				# self.__speed_x -= PLAYER_SPEED_X / 2
				self.__bLookRight = False
				self.__bBreak = True
			else:
				# Running
				self.__bLookRight = False
				if self.__bBreak:
					# if self.__speed_x <= -PLAYER_SPEED_X / 2:
					self.__bBreak = False

		if is_pressed('right'):
			bKeyPressed = True
			self.__bRunning = True

			# Speed Setting
			self.__dir += 1

			# Flag Setting
			if self.__speed_x < 0:
				# Breaking
				# self.__speed_x += PLAYER_SPEED_X / 2
				self.__bLookRight = True
				self.__bBreak = True
			else:
				# Running
				self.__bLookRight = True
				if self.__bBreak:
					# if self.__speed_x >= PLAYER_SPEED_X / 2:
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
			# self.__speed_x -= PLAYER_SPEED_X / 3
			if self.__speed_x < 0:
				self.__speed_x = 0

		elif self.__speed_x < 0:
			# self.__speed_x += PLAYER_SPEED_X / 3
			if self.__speed_x > 0:
				self.__speed_x = 0

		if not bKeyPressed:
			self.__bBreak = False
		# Move End

		if self.__size == 2 and is_pressed('ctrl'):
			if not self.__bAttack:
				self.__bAttack = True
				# Make bullet here
				bullet = Bullet.Bullet(self.__x + Tile.TILE_SIZE * (1 - 2 * (not self.__bLookRight)), self.__y,
									   self.__bLookRight)
				main_state.bullets.append(bullet)
				main_state.game_objects.add_object(bullet, 2)
		else:
			self.__bAttack = False

		return None

	# Input End
	def is_invincible(self):
		return self.__bInvincible

	# returns is still alive
	def size_down(self):
		self.__size -= 1
		if self.__size < 0:
			return False
		self.__bInvincible = True
		self.__invincible_timer = 0.0
		return True

	def go_x_back(self):
		self.__x = self.__bef_x
		self.__speed_x = 0

	def land(self, y_pos):
		self.__speed_y = 0
		self.__y = y_pos + Tile.TILE_SIZE
		self.__bJump = False
		self.__bFalling = False

	def is_jumping(self):
		return self.__bJump or self.__bFalling

	def update(self):
		self.__bef_x = self.__x
		self.__bef_y = self.__y

		if self.__bInvincible:
			self.__invincible_timer += game_framework.frame_time
			if self.__invincible_timer >= 5.0:
				self.__bInvincible = False
				self.__invincible_timer = 0.0

		# x axis
		# accelerate, breaking
		dx = PLAYER_SPEED_PPS * game_framework.frame_time * 2

		# break
		if self.__bBreak:
			dx *= 1.5

		if self.__dir > 0:
			self.__speed_x += dx
			if self.__speed_x >= PLAYER_SPEED_PPS:
				self.__speed_x = PLAYER_SPEED_PPS
		elif self.__dir < 0:
			self.__speed_x -= dx
			if self.__speed_x <= -PLAYER_SPEED_PPS:
				self.__speed_x = -PLAYER_SPEED_PPS
		else:
			if self.__speed_x > 0:
				self.__speed_x -= dx
				if self.__speed_x < 0:
					self.__speed_x = 0
			elif self.__speed_x < 0:
				self.__speed_x += dx
				if self.__speed_x > 0:
					self.__speed_x = 0
		self.__x += self.__speed_x * game_framework.frame_time

		# y axis
		self.__speed_y -= 12 * PIXEL_PER_METER * game_framework.frame_time
		if self.__speed_y < -PLAYER_TERMINAL_VELOCITY_PPS:
			self.__speed_y = -PLAYER_TERMINAL_VELOCITY_PPS

		self.__y += self.__speed_y * game_framework.frame_time

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

		# frame update
		# Set Img Sprite
		bFrame = False

		# Image sprite priority
		# attack > jump > sit > break > running > idle
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

		# Set Frame
		if bFrame:
			# self.__frame = (self.__frame + 1) % 40
			self.__frame = (
									   self.__frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
		else:
			self.__frame = 0

		self.__characterImageSprite.clip_draw(
			(self.__imgSprite + (bFrame * int(self.__frame))) * 17 + 153 * self.__bLookRight,
			(2 - self.__size) * 33,
			16, 32, self.__x - main_state.screen_offset, self.__y,
			Tile.TILE_SIZE,
			Tile.TILE_SIZE + Tile.TILE_SIZE - ((self.__bSitDown or self.__size == 0) * Tile.TILE_SIZE) / 2)

	# draw_rectangle(*(self.get_position()))

	# Draw End

	def get_x(self):
		return self.__x

	# returns true when dir == right
	def get_dir(self):
		return self.__bLookRight

	def get_size(self):
		return self.__size

	def set_size(self, size):
		self.__size = size
# Test Funcs
# def sprite_up(self):
# 	self.__imgSprite += 1
#
# def sprite_down(self):
# 	self.__imgSprite -= 1
#
# def size_up(self):
# 	self.__size += 1


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

		# mario.move()
		delay(0.01)

		clear_canvas()
		mario.draw()
		update_canvas()
	close_canvas()
