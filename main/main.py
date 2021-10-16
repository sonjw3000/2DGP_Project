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
		self.max_x_index = 20
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

	def __collide_check(self):
		# collide check here
		bLand = False
		xCol = False
		l, b, r, t = self.mario.get_position()

		left_index = int((l - 1) // Tile.TILE_SIZE)
		bottom_index = int((b - 1) // Tile.TILE_SIZE)
		right_index = int(r // Tile.TILE_SIZE)
		top_index = int(t // Tile.TILE_SIZE)

		# Check X block
		# Right with block
		if left_index < 0:
			xCol = self.mario.go_x_back()
			left_index = 0
		elif right_index >= self.max_x_index:
			xCol = self.mario.go_x_back()
			right_index = self.max_x_index - 1
		elif self.tiles[bottom_index + 1][left_index].get_is_collidable() or \
				self.tiles[top_index][left_index].get_is_collidable():
			xCol = self.mario.go_x_back()
		elif self.tiles[bottom_index + 1][right_index].get_is_collidable() or \
				self.tiles[top_index][right_index].get_is_collidable():
			xCol = self.mario.go_x_back()

		# Falling Check
		# Check Y axis Collide
		if bottom_index < 0:
			# PlayerDead
			pass
		elif self.tiles[bottom_index][left_index].get_is_collidable() or \
				self.tiles[bottom_index][right_index].get_is_collidable():
			bLand = True
		elif self.tiles[top_index][left_index].get_is_collidable(True) or \
				self.tiles[top_index][right_index].get_is_collidable(True):
			# hit bottom of the box
			# * -1 jump speed
			if self.mario.hit_ceil():
				# break tile
				self.tiles[int(top_index)][int(left_index)].collide()
				self.tiles[int(top_index)][int(right_index)].collide()

		# Monster Y Check
		# pass

		return (bLand * Tile.TILE_SIZE * (bottom_index + 1)), xCol

	def update(self):
		yCol, xCol = self.__collide_check()
		for line in self.tiles:
			for t in line:
				t.update()

		self.mario.move(yCol, xCol)

		pass

	# Update End

	def draw(self):
		clear_canvas()

		for line in self.tiles:
			for t in line:
				t.draw()

		for line in self.tiles:
			for t in line:
				t.draw_breaking()

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
