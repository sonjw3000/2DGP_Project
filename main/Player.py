from pico2d import *
from keyboard import is_pressed


# import keyboard


class Player:
	def __init__(self, x=10, y=100, size=2):
		# Init Image Sprite
		self.__characterImageSprite = load_image('./resource/Mario_Real.png')

		# Mario Moving bool variables
		self.__bRunning = False

		# Set Pos
		self.__x = x
		self.__y = y

		# Mario Current Size
		self.__size = size

		# Mario Move Direction -1 : left, 0 : Idle, 1 : Right
		self.__imgSprite = 0
		self.__bLookRight = True

		self.__speed = 0

		self.__bBreak = False
		self.__bSitDown = False

	# Constructor End

	# Returns Left, Bottom, Right, Top
	def get_position(self):
		return self.__x, self.__y, self.__x + 16, self.__y + 16 + (self.__size != 0) * (self.__bSitDown != 0) * 16

	def input(self):
		bKeyPressed = False
		if is_pressed('left'):
			bKeyPressed = True
			# Speed Setting
			if self.__speed > -1:
				self.__speed -= 0.05
			else:
				self.__speed = -1

			# Image Sprite Setting
			if self.__speed > 0:
				# Breaking
				self.__speed -= 0.03
				self.__bLookRight = False
				self.__imgSprite = 7

				self.__bBreak = True
			else:
				# Running
				self.__bLookRight = False
				self.__imgSprite = 0

				if self.__bBreak:
					if self.__speed > -0.3:
						self.__imgSprite = 7
					else:
						self.__bBreak = False

		if is_pressed('right'):
			bKeyPressed = True
			# Speed Setting
			if self.__speed < 1:
				self.__speed += 0.05
			else:
				self.__speed = 1

			# Image Sprite Setting
			if self.__speed < 0:
				# Breaking
				self.__speed += 0.03
				self.__bLookRight = True
				self.__imgSprite = 7
			else:
				# Running
				self.__bLookRight = True
				self.__imgSprite = 0

				if self.__bBreak:
					if self.__speed < 0.3:
						self.__imgSprite = 7
					else:
						self.__bBreak = False

		if is_pressed('down'):
			bKeyPressed = True
			self.__bSitDown = True
		else:
			self.__bSitDown = False

		if is_pressed('up'):
			bKeyPressed = True
			print("up")

		# Slow Down
		if self.__speed > 0:
			self.__speed -= 0.02
			if self.__speed < 0:
				self.__speed = 0

		elif self.__speed < 0:
			self.__speed += 0.02
			if self.__speed > 0:
				self.__speed = 0

		if not bKeyPressed: 		# and not jumping
			self.__imgSprite = 0
			self.__bBreak = False

	# Input End

	def move(self):
		self.__x += self.__speed

	def draw(self):
		# print(self.__speed)
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
		if self.__speed == 0 and not self.__bBreak:
			self.__imgSprite = 0

		if self.__bSitDown:		# and not jumping
			self.__imgSprite = 8

		self.__characterImageSprite.clip_draw(
			self.__imgSprite * 17 + 153 * self.__bLookRight,
			(2 - self.__size) * 33,
			16, 32, self.__x, self.__y)

	# Draw End

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
	mario = Player()

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
