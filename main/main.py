from pico2d import *
# from pynput import keyboard
# import keyboard
import Player


# All rectangle have left, bottom position as their offset

class GameRunner:
	def __init__(self):
		# init game here
		self.bGameLoop = True

		# Game Objects
		self.mario = Player.Player()

	# Constructor end

	def __handle_events(self):
		game_events = get_events()
		for event in game_events:
			if event.type == SDL_QUIT:
				self.bGameLoop = False
			elif event.type == SDL_KEYDOWN:
				if event.key == SDLK_ESCAPE:
					self.bGameLoop = False

	# Event handler End

	def input(self):
		self.__handle_events()
		self.mario.input()

	# Input End

	def update(self):
		self.mario.move()
		# collide check here
		# fill
		pass

	# Update End

	def draw(self):
		clear_canvas()

		self.mario.draw()
		update_canvas()
# Draw End


# Class End


def main():
	# Init game Settings
	open_canvas()
	game = GameRunner()

	# Game Loop
	while game.bGameLoop:
		game.input()
		game.update()
		game.draw()
		delay(0.01)

	close_canvas()


if __name__ == "__main__":
	main()
