from GameWorld import *
from pico2d import *
import Player
import Monster
import Bullet
import Tile
import game_framework

# for test
import TestMap

gamePlayer = None
monsters = None
bullets = None
tiles = None

game_objects = GameObjects()


def test():
	global game_objects
	# Tiles

	global tiles
	tiles = []
	for i in range(15):
		tiles.append([])
		for j in range(20):
			game_objects.add_object(TestMap.TestMap[i][j], 0)
			tiles[i].append(TestMap.TestMap[i][j])

	# Monsters
	global monsters
	monsters = []

	for i in TestMap.Monster:
		game_objects.add_object(i, 2)
		monsters.append(i)

	# Player
	global gamePlayer
	gamePlayer = Player.Player()
	game_objects.add_object(gamePlayer, 3)
	tileImage = load_image('./resource/tiles/overworld.png')
	Tile.Tile.set_image(tileImage)

	bulletImg = load_image('./resource/bullets.png')
	Bullet.Bullet.set_image(bulletImg)

	monsterImg = load_image("./resource/monsters.png")
	Monster.Monster.set_image(monsterImg)


def collide_check(a, b):
	left_a, bottom_a, right_a, top_a = a.get_position()
	left_b, bottom_b, right_b, top_b = b.get_position()
	if left_a > right_b: return False
	if right_a < left_b: return False
	if top_a < bottom_b: return False
	if bottom_a > top_b: return False
	return True


# returns x, y collide, if out of range, return None
def tile_collide_check(box):
	left, bottom, right, top = box.get_position()
	left_index = int((left - 1) // Tile.TILE_SIZE)
	bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
	right_index = int(right // Tile.TILE_SIZE)
	top_index = int(top // Tile.TILE_SIZE)

	xCol = False
	yCol = False

	# x collide check here
	if left_index < 0:
		xCol = True
		left_index = 0
	elif right_index >= len(tiles[0]):
		xCol = True
		right_index = len(tiles[0]) - 1
	elif tiles[bottom_index + 1][left_index].get_is_collidable() or \
			tiles[top_index][left_index].get_is_collidable():
		xCol = True
	elif tiles[bottom_index + 1][right_index].get_is_collidable() or \
			tiles[top_index][right_index].get_is_collidable():
		xCol = True

	# y collide check here
	if bottom_index < 0:
		# Player dead or Bullet dead
		return None
	elif tiles[bottom_index][left_index].get_is_collidable() or \
			tiles[bottom_index][right_index].get_is_collidable():
		yCol = True
	elif (tiles[top_index][left_index].get_is_collidable(True) or \
		  tiles[top_index][right_index].get_is_collidable(True)):
		yCol = True

	return xCol, yCol * (bottom_index + 1)


def enter():
	# game_objects.load_objects_from_file("")
	test()


def exit():
	pass


def handle_events():
	gamePlayer.input()

	game_events = get_events()
	for event in game_events:
		if event.type == SDL_QUIT:
			game_framework.exit_program()

		elif event.type == SDL_KEYDOWN:
			if event.key == SDLK_ESCAPE:
				game_framework.exit_program()


def update():
	for objs in game_objects.all_objects():
		objs.update()

	x, y = tile_collide_check(gamePlayer)
	print(x, y)


def draw():
	clear_canvas()
	for objs in game_objects.all_objects():
		objs.draw()
	update_canvas()


def pause():
	pass


def resume():
	pass
