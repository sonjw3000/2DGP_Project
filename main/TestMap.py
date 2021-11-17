from Tile import *
from pico2d import *
from Bullet import *
# from pynput import keyboard
# import keyboard
import Player
import Monster
import main_this_is_trash


# 800, 600

# 맵툴을 만들자 제발
# 가로 20, 세로 15

TestMapTile = [
	[Tile(TILE_SIZE * i, TILE_SIZE * 0, True, False, 0) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 1, False + (i == 19 or i == 14), False, 56 - 56 * (i == 19 or i == 14)) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 2, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 3, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 4, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 5, True, True, 33) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 6, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 7, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 8, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 9, False, False, 56, (i // 10) * 4) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 10, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 11, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 12, False, False, 56) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 13, True, True, 33 + 31 * (i >= 10), 3) for i in range(40)],
	[Tile(TILE_SIZE * i, TILE_SIZE * 14, False, False, 56) for i in range(40)],
]

Monster = [
	Monster.Monster(700, 70, 1, False)
]

if __name__ == "__main__":
	# Init game Settings
	open_canvas()

	game = main_this_is_trash.GameRunner()

	game.init_game()
	game.tiles = TestMapTile
	game.monsters = Monster

	# Game Loop
	while game.bGameLoop:
		game.input()
		game.update()
		game.draw()
		delay(0.01)

	close_canvas()
