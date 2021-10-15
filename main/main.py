from pico2d import *
# from pynput import keyboard
# import keyboard
import Player
import Tile


# All rectangle have left, bottom position as their offset

class GameRunner:
	def __init__(self):
		# init game here

		self.bGameLoop = True

		# Game Objects
		self.mario = Player.Player(80, 80, 2)
		self.tiles = [Tile.Tile(0, 0, True, True, 0)]

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
		# collide check here
		bLand = False
		l, b, r, t = self.mario.get_position()

		# Falling Check
		left_index = (l - 1) // Tile.TILE_SIZE
		bottom_index = (b - 1) // Tile.TILE_SIZE
		right_index = (r + 1) // Tile.TILE_SIZE
		top_index = (t + 1) // Tile.TILE_SIZE

		if bottom_index < 0:
			# PlayerDead
			pass
		elif self.tiles[int(bottom_index)][int(left_index)].get_is_collidable() or self.tiles[int(bottom_index)][int(right_index)].get_is_collidable():
			bLand = True

		# fill

		self.mario.move(bLand * 40)

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
