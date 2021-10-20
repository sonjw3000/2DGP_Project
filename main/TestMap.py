from Tile import *
from pico2d import *
from Bullet import *
# from pynput import keyboard
# import keyboard
import Player
import main

# 800, 600

# 맵툴을 만들자 제발
# 가로 20, 세로 15
TestMap = [
	[
		Tile(TILE_SIZE * i, TILE_SIZE * 0, True, False, 0) for i in range(20)
	],
	[Tile(TILE_SIZE * i, TILE_SIZE * 1, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 2, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 3, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 4, True, True, 33) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 5, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 6, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 7, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 8, False, False, 56, i // 10) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 9, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 10, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 11, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 12, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 13, False, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 14, False, False, 56) for i in range(20)],
]

if __name__ == "__main__":
	# Init game Settings
	open_canvas()

	game = main.GameRunner()

	game.init_game()
	game.tiles = TestMap

	# Game Loop
	while game.bGameLoop:
		game.input()
		game.update()
		game.draw()
		delay(0.01)

	close_canvas()
