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
items = None

game_objects = GameObjects()

current_stage = 0
player_life = 5


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
	gamePlayer = Player.Player(50, 80)
	game_objects.add_object(gamePlayer, 3)

	# item
	global items
	items = []

	# load img
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
def tile_collide_check(left, bottom, right, top):
	left_index = int((left + 1) // Tile.TILE_SIZE)
	bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
	right_index = int((right - 1) // Tile.TILE_SIZE)
	top_index = int(top // Tile.TILE_SIZE)

	xCol = False
	yCol = False

	if bottom_index < 0:
		# Player dead or Bullet dead
		return None

	# x collide check here
	if left_index < 0:
		xCol = -1
		left_index = 0
	elif right_index >= len(tiles[0]):
		xCol = 1
		right_index = len(tiles[0]) - 1
	elif tiles[bottom_index + 1][left_index].get_is_collidable() or \
			tiles[top_index][left_index].get_is_collidable():
		xCol = -1
	elif tiles[bottom_index + 1][right_index].get_is_collidable() or \
			tiles[top_index][right_index].get_is_collidable():
		xCol = 1

	# y collide check here
	if tiles[bottom_index][left_index].get_is_collidable() or \
			tiles[bottom_index][right_index].get_is_collidable():
		yCol = -1
	elif (tiles[top_index][left_index].get_is_collidable(True) or \
		  tiles[top_index][right_index].get_is_collidable(True)):
		yCol = 1

	return xCol, yCol * (bottom_index + 1)


def tile_collide_check_x(left, bottom, right, top):
	left_index = int((left + 1) // Tile.TILE_SIZE)
	bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
	right_index = int((right - 1) // Tile.TILE_SIZE)
	top_index = int(top // Tile.TILE_SIZE)

	xCol = False

	if bottom_index < 0:
		# Player dead or Bullet dead
		return None

	# x collide check here
	if left_index < 0:
		xCol = -1
		left_index = 0
	elif right_index >= len(tiles[0]):
		xCol = 1
		right_index = len(tiles[0]) - 1
	elif tiles[bottom_index + 1][left_index].get_is_collidable() or \
			tiles[top_index][left_index].get_is_collidable():
		xCol = -1
	elif tiles[bottom_index + 1][right_index].get_is_collidable() or \
			tiles[top_index][right_index].get_is_collidable():
		xCol = 1

	return xCol


def tile_collide_check_y(left, bottom, right, top):
	left_index = int((left + 1) // Tile.TILE_SIZE)
	bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
	right_index = int((right - 1) // Tile.TILE_SIZE)
	top_index = int(top // Tile.TILE_SIZE)

	yCol = False

	if bottom_index < 0:
		# Player dead or Bullet dead
		return None

	# y collide check here
	if tiles[bottom_index][left_index].get_is_collidable() or \
			tiles[bottom_index][right_index].get_is_collidable():
		yCol = -1
	elif (tiles[top_index][left_index].get_is_collidable(True) or \
		  tiles[top_index][right_index].get_is_collidable(True)):
		yCol = 1

	return yCol * (bottom_index + 1)


def enter():
	global current_stage
	current_stage += 1
	str = "어쨋든 스테이지 파일임_" + current_stage.__str__()

	global bullets
	bullets = []
	# game_objects.load_objects_from_file(str)
	test()


def exit():
	game_objects.clear()
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
	# move everything
	for objs in game_objects.all_objects():
		objs.update()

	# player-tile collide
	# check x col
	state = tile_collide_check_x(*(gamePlayer.get_position()))
	if state is not None:
		x_collide = state
		if x_collide:
			gamePlayer.go_x_back()
	# check y col
	state = tile_collide_check_y(*(gamePlayer.get_position()))
	if state is not None:
		y_collide = state
		if y_collide:
			if y_collide > 0:
				if gamePlayer.hit_ceil():
					l, b, r, t = gamePlayer.get_position()

					left_index = int((l + 1) // Tile.TILE_SIZE)
					right_index = int((r - 1) // Tile.TILE_SIZE)
					top_index = int(t // Tile.TILE_SIZE)

					tiles[top_index][left_index].collide()
					tiles[top_index][right_index].collide()
			else:
				gamePlayer.land(y_collide * Tile.TILE_SIZE * -1)
	else:
		print("player out")

	# bullets
	for bullet in bullets:
		state = tile_collide_check_x(*(bullet.get_position()))
		if state is not None:
			x_collide = state
			if x_collide:
				game_objects.remove_object(bullet)
				bullets.remove(bullet)
				continue

		state = tile_collide_check_y(*(bullet.get_position()))
		if state is not None:
			y_collide = state
			if y_collide:
				bullet.hit_floor()
		else:
			game_objects.remove_object(bullet)
			bullets.remove(bullet)
			continue
		# bullet timer
		if not bullet.is_still_alive():
			game_objects.remove_object(bullet)
			bullets.remove(bullet)

	# monsters
	for monster in monsters:
		# player-monster collide
		if collide_check(monster, gamePlayer) and not gamePlayer.is_invincible():
			if not gamePlayer.size_down():
				# reload cur stage
				global player_life
				player_life -= 1
				if player_life < 0:
					# goto start state
					# exit cur state
					#
					return
				else:
					# reload cur state
					global current_stage
					current_stage -= 1
					exit()
					enter()
					return

		# monster-tile collide
		state = tile_collide_check(*(monster.get_position()))
		if state != None:
			x_collide, y_collide = state
			if x_collide:
				monster.reverse()
			if y_collide:
				monster.land(y_collide * Tile.TILE_SIZE * -1)
		else:
			print("monster out")

		# monster-bullet collide
		for bullet in bullets:
			if collide_check(bullet, monster):
				game_objects.remove_object(bullet)
				game_objects.remove_object(monster)
				bullets.remove(bullet)
				monsters.remove(monster)
				continue


def draw():
	clear_canvas()
	for objs in game_objects.all_objects():
		objs.draw()

	for line in tiles:
		for t in line:
			t.draw_breaking()

	update_canvas()


def pause():
	pass


def resume():
	pass
