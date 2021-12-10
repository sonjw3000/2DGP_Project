from pico2d import *
from keyboard import is_pressed
# from Tile import TILE_SIZE
# import Tile
import Bullet
import game_framework
import GameWorld
import main_state
import server
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

PLAYER_SIZE = 40

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
	characterImageSprite = None

	def __init__(self, x=8, y=16, size=2):
		# Mario Moving bool variables
		self.bRunning = False
		self.bBreak = False
		self.bSitDown = False
		self.bRunning = False
		self.bAttack = False
		self.bJump = False
		self.bFalling = False
		self.bDead = False

		# invincible control variables
		self.bInvincible = False
		self.invincible_timer = 0.0

		# Set Pos
		self.x = x
		self.y = y

		# bef pos
		self.bef_x = x
		self.bef_y = y

		# Mario Current Size
		self.size = size

		# Mario Move Direction -1 : left, 0 : Idle, 1 : Right
		self.imgSprite = 0
		self.frame = 0
		self.bLookRight = True

		self.speed_x = 0
		self.speed_y = 0

		self.dir = 0

		self.yMove = 0

	# Constructor End

	# Returns rectangle tuple (Left, Bottom, Right, Top)
	def get_position(self):
		return (self.x - PLAYER_SIZE / 2,
				self.y - PLAYER_SIZE,
				self.x + PLAYER_SIZE / 2,
				self.y + PLAYER_SIZE - ((self.bSitDown or self.size == 0) * PLAYER_SIZE))

	def hit_ceil(self):
		if self.speed_y <= 0:
			return False

		self.speed_y *= -1
		self.bFalling = True
		return True

	def input(self):
		self.dir = 0
		bKeyPressed = False
		self.bRunning = False

		# Move Start
		if is_pressed('left'):
			bKeyPressed = True
			self.bRunning = True

			# Speed Setting
			self.dir -= 1

			# Flag Setting
			if self.speed_x > 0:
				# Breaking
				# self.speed_x -= PLAYER_SPEED_X / 2
				self.bLookRight = False
				self.bBreak = True
			else:
				# Running
				self.bLookRight = False
				if self.bBreak:
					# if self.speed_x <= -PLAYER_SPEED_X / 2:
					self.bBreak = False

		if is_pressed('right'):
			bKeyPressed = True
			self.bRunning = True

			# Speed Setting
			self.dir += 1

			# Flag Setting
			if self.speed_x < 0:
				# Breaking
				# self.speed_x += PLAYER_SPEED_X / 2
				self.bLookRight = True
				self.bBreak = True
			else:
				# Running
				self.bLookRight = True
				if self.bBreak:
					# if self.speed_x >= PLAYER_SPEED_X / 2:
					self.bBreak = False

		if is_pressed('down'):
			bKeyPressed = True
			self.bSitDown = True
		else:
			self.bSitDown = False

		if is_pressed('up'):
			# jump gogo
			bKeyPressed = True
			if not self.bFalling:
				self.speed_y = PLAYER_TERMINAL_VELOCITY_PPS
				self.bJump = True
				self.yMove += self.speed_y
				game_framework.jump_bgm.play(1)
			if self.yMove >= PLAYER_MAX_JUMP_HEIGHT:
				self.bFalling = True
		else:
			self.bFalling = True

		# Slow Down
		if self.speed_x > 0:
			# self.speed_x -= PLAYER_SPEED_X / 3
			if self.speed_x < 0:
				self.speed_x = 0

		elif self.speed_x < 0:
			# self.speed_x += PLAYER_SPEED_X / 3
			if self.speed_x > 0:
				self.speed_x = 0

		if not bKeyPressed:
			self.bBreak = False
		# Move End

		if self.size == 2 and is_pressed('ctrl'):
			if not self.bAttack:
				self.bAttack = True
				# Make bullet here
				game_framework.fire_ball_bgm.play(1)
				bullet = Bullet.Bullet(self.x + PLAYER_SIZE * (1 - 2 * (not self.bLookRight)), self.y,
									   self.bLookRight)
				server.bullets.append(bullet)
				GameWorld.add_object(bullet, 2)
		else:
			self.bAttack = False

		return None

	# Input End
	def is_invincible(self):
		return self.bInvincible

	# returns is still alive
	def size_down(self):
		self.size -= 1
		if self.size < 0:
			return False
		server.playerSize -= 1
		self.bInvincible = True
		self.invincible_timer = 0.0
		game_framework.size_down_bgm.play(1)
		return True

	def go_x_back(self):
		self.x = self.bef_x
		self.speed_x = 0

	def land(self, y_pos):
		self.speed_y = 0
		self.y = y_pos + PLAYER_SIZE
		self.bJump = False
		self.bFalling = False

	def is_jumping(self):
		return self.bJump or self.bFalling

	def update(self):
		self.bef_x = self.x
		self.bef_y = self.y

		if self.bInvincible:
			self.invincible_timer += game_framework.frame_time
			if self.invincible_timer >= 5.0:
				self.bInvincible = False
				self.invincible_timer = 0.0

		# x axis
		# accelerate, breaking
		dx = PLAYER_SPEED_PPS * game_framework.frame_time * 2

		# break
		if self.bBreak:
			dx *= 1.5

		if self.dir > 0:
			self.speed_x += dx
			if self.speed_x >= PLAYER_SPEED_PPS:
				self.speed_x = PLAYER_SPEED_PPS
		elif self.dir < 0:
			self.speed_x -= dx
			if self.speed_x <= -PLAYER_SPEED_PPS:
				self.speed_x = -PLAYER_SPEED_PPS
		else:
			if self.speed_x > 0:
				self.speed_x -= dx
				if self.speed_x < 0:
					self.speed_x = 0
			elif self.speed_x < 0:
				self.speed_x += dx
				if self.speed_x > 0:
					self.speed_x = 0
		self.x += self.speed_x * game_framework.frame_time

		# y axis
		self.speed_y -= 12 * PIXEL_PER_METER * game_framework.frame_time
		if self.speed_y < -PLAYER_TERMINAL_VELOCITY_PPS:
			self.speed_y = -PLAYER_TERMINAL_VELOCITY_PPS

		self.y += self.speed_y * game_framework.frame_time

	def draw(self):
		# print(self.speed_x)
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
		self.imgSprite = 0
		if self.bDead:
			self.imgSprite = 6
		elif self.bAttack:
			self.imgSprite = 6
		elif self.bJump or self.bFalling:
			self.imgSprite = 1
		elif self.bSitDown:
			self.imgSprite = 8
		elif self.bBreak and self.size:
			self.imgSprite = 7
		elif self.bRunning:
			self.imgSprite = 2
			bFrame = True

		# Set Frame
		if bFrame:
			# self.frame = (self.frame + 1) % 40
			self.frame = \
				(self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
				FRAMES_PER_ACTION
		else:
			self.frame = 0

		Player.characterImageSprite.clip_draw(
			(self.imgSprite + (bFrame * int(self.frame))) * 17 + 153 * self.bLookRight,
			(2 - self.size) * 33,
			16, 32, self.x - main_state.screen_offset, self.y - ((self.bSitDown or self.size == 0) * PLAYER_SIZE) / 4,
			PLAYER_SIZE,
			PLAYER_SIZE + PLAYER_SIZE - ((self.bSitDown or self.size == 0) * PLAYER_SIZE) / 2)

	def dead(self):
		server.playerSize = 0
		self.speed_y = 300
		self.size = 0
		self.bDead = True

	def bounce(self):
		self.speed_y = 200
		self.y += self.speed_y * game_framework.frame_time

	def draw_dead(self):
		Player.characterImageSprite.clip_draw(
			6 * 17 + 153 * self.bLookRight,
			2 * 33,
			16, 16, self.x - main_state.screen_offset, self.y,
			PLAYER_SIZE,
			PLAYER_SIZE)

	# returns true when out of screen모듈
	def dead_update(self):
		self.speed_y -= 12 * PIXEL_PER_METER * game_framework.frame_time
		if self.speed_y < -PLAYER_TERMINAL_VELOCITY_PPS:
			self.speed_y = -PLAYER_TERMINAL_VELOCITY_PPS

		self.y += self.speed_y * game_framework.frame_time

		return self.y < -20

	# returns true when on floor
	def goal_update(self):
		self.y -= PLAYER_SPEED_PPS * 0.5 * game_framework.frame_time
		return self.y <= PLAYER_SIZE * 2

	def goal_update_2(self):
		self.x += PLAYER_SPEED_PPS * 0.3 * game_framework.frame_time
		self.bRunning = True
		self.bJump = False
		self.bFalling = False
	# draw_rectangle(*(self.get_position()))

	@classmethod
	def set_image(cls, player_img):
		cls.characterImageSprite = player_img

	def __getstate__(self):
		# x, y, dir, size
		state = {'x': self.x, 'y': self.y, 'dir': self.dir, 'size': self.size}
		return state

	def __setstate__(self, state):
		self.__init__(2, 3, 2)
		self.__dict__.update(state)

	# Draw End

	def get_x(self):
		return self.x

	# returns true when dir == right
	def get_dir(self):
		return self.bLookRight

	def get_size(self):
		return self.size

	def set_size(self, size):
		server.playerSize = size
		if self.size < size:
			game_framework.power_up_bgm.play(1)

		self.size = size


# Test Funcs
# def sprite_up(self):
# 	self.imgSprite += 1
#
# def sprite_down(self):
# 	self.imgSprite -= 1
#
# def size_up(self):
# 	self.size += 1


# Test Funcs End


# Class End


# Mario Test
if __name__ == "main":
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
