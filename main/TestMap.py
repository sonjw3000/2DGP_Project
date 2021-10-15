from Tile import *
from pico2d import *
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
	[Tile(TILE_SIZE * i, TILE_SIZE * 1, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 2, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 3, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 4, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 5, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 6, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 7, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 8, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 9, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 10, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 11, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 12, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 13, True, False, 56) for i in range(20)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 14, True, False, 56) for i in range(20)],
]

if __name__ == "__main__":
	# Init game Settings
	open_canvas()
	game = main.GameRunner()
	tileImage = load_image('./resource/tiles/overworld.png')
	Tile.set_image(tileImage)

	game.tiles = TestMap

	# Game Loop
	while game.bGameLoop:
		game.input()
		game.update()

		clear_canvas()
		for line in TestMap:
			for t in line:
				t.draw()
		game.mario.draw()
		update_canvas()
		# game.draw()
		delay(0.01)

	close_canvas()
