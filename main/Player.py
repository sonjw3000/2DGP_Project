from pico2d import *
from keyboard import is_pressed
#import keyboard


class Player:
	def __init__(self, x = 10, y = 100, size = 2):
		# Init Image Sprite
		self.__characterImageSprite = load_image('resource\\Mario_Real.png')

		# Mario Moving bool variables
		self.__bRunning = False

		# Set Pos
		self.__x = x
		self.__y = y

		# Mario Current Size
		self.__size = size

		# Mario Move Direction -1 : left, 0 : Idle, 1 : Right
		self.__dir = 0
		self.__imgSprite = 0
		self.__bLookRight = True

		self.__speed = 0

		self.__bBreak = False
	# Constructor End

	# Returns Left, Bottom, Right, Top
	def getPosition(self):	
		return self.__x, self.__y, self.__x + 16, self.__y + 16 + (self.__size != 0) * 16


	def input(self):
		if is_pressed('left'):
			# Speed Setting
			if self.__speed > -1:	self.__speed -= 0.05
			else: 					self.__speed = -1
			
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
			# Speed Setting
			if self.__speed < 1:	self.__speed += 0.05
			else: 					self.__speed = 1

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
			print("down")

		if is_pressed('up'):
			print("up")

		# Slow Down
		if self.__speed > 0: 
			self.__speed -= 0.02
			if self.__speed < 0: self.__speed = 0
		elif self.__speed < 0: 
			self.__speed += 0.02
			if self.__speed > 0: self.__speed = 0
		




	def move(self):
		self.__x += self.__speed


	def draw(self):
		#print(self.__speed)
		# img start pos (0,1)
		# x offset : 17
		# y offset : 33
		# character size : 16 x 32, if size == 0, 16 x 16

		# Sprite 0 : Idle
		# Sprite 1 : Jump
		# Sprite 2 ~ 5 : Run
		# Sprite 6 : Attack(Size : 2), Empty(Size : 1), Dead(Size : 0)
		# Sprite 7 : Sit Down
		if self.__speed == 0 and not self.__bBreak: self.__imgSprite = 0

		self.__characterImageSprite.clip_draw(
			self.__imgSprite * 17 + 153 * self.__bLookRight, 
			(2 - self.__size) * 33, 
			16, 32, self.__x, self.__y)
	# Draw End


	# Test Funcs
	def spriteUp(self):
		self.__imgSprite += 1

	def spriteDown(self):
		self.__imgSprite -= 1

	def sizeUp(self):
		self.__size += 1

	def sizeDown(self):
		self.__size -= 1
	# Test Funcs End
    
# Class End