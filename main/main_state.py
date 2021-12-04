from GameWorld import *
from pico2d import *
import Player
import Monster
import Bullet
import Tile
import game_framework
import copy

import server

# for test
import TestMap

font = None

game_objects = GameObjects()

current_stage = 0

# game var
player_life = 5
game_score = 0
game_coin = 0
game_time = 300

screen_offset = 0

def test():
	global game_objects
	# Tiles


	server.tiles = []
	for lists in TestMap.TestMapTile:
		server.tiles.append(lists)

	for i in range(len(server.tiles) - 1, 0 - 1, -1):
		game_objects.add_objects(server.tiles[i][::-1], 0)

	# Monsters
	server.monsters = []
	server.monsters = copy.deepcopy(TestMap.Monster)

	game_objects.add_objects(server.monsters, 2)

	# Player
	server.gamePlayer = Player.Player(50, 80, 0)
	game_objects.add_object(server.gamePlayer, 3)

	# item
	server.items = []

	# load img
	tileImage = load_image('./resource/tiles/overworld.png')
	Tile.Tile.set_image(tileImage)

	bulletImg = load_image('./resource/bullets.png')
	Bullet.Bullet.set_image(bulletImg)

	monsterImg = load_image("./resource/monsters.png")
	Monster.Monster.set_image(monsterImg)

	global font
	font = load_font('./resource/ENCR10B.TTF', 16)


def check_collide(a, b):
	left_a, bottom_a, right_a, top_a = a.get_position()
	left_b, bottom_b, right_b, top_b = b.get_position()
	if left_a > right_b: return False
	if right_a < left_b: return False
	if top_a < bottom_b: return False
	if bottom_a > top_b: return False
	return True


# returns x, y collide, if out of range, return None
def check_tile_collide(left, bottom, right, top):
	left_index = int((left + 1) // Tile.TILE_SIZE)
	bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
	right_index = int((right - 1) // Tile.TILE_SIZE)
	top_index = int(top // Tile.TILE_SIZE)

	xCol = False
	yCol = False

	if bottom_index < 0:
		# something dead
		return None

	# x collide check here
	if left_index < 0:
		xCol = -1
		left_index = 0
	elif right_index >= len(server.tiles[0]):
		xCol = 1
		right_index = len(server.tiles[0]) - 1
	elif server.tiles[bottom_index + 1][left_index].get_is_collidable() or \
			server.tiles[top_index][left_index].get_is_collidable():
		xCol = -1
	elif server.tiles[bottom_index + 1][right_index].get_is_collidable() or \
			server.tiles[top_index][right_index].get_is_collidable():
		xCol = 1

	# y collide check here
	if server.tiles[bottom_index][left_index].get_is_collidable() or \
			server.tiles[bottom_index][right_index].get_is_collidable():
		yCol = -1
	elif (server.tiles[top_index][left_index].get_is_collidable() or \
		  server.tiles[top_index][right_index].get_is_collidable()):
		yCol = 1

	return xCol, yCol * (bottom_index + 1)


def check_tile_collide_x(left, bottom, right, top):
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
	elif right_index >= len(server.tiles[0]):
		xCol = 1
		right_index = len(server.tiles[0]) - 1
	elif server.tiles[bottom_index + 1][left_index].get_is_collidable() or \
			server.tiles[top_index][left_index].get_is_collidable():
		xCol = -1
	elif server.tiles[bottom_index + 1][right_index].get_is_collidable() or \
			server.tiles[top_index][right_index].get_is_collidable():
		xCol = 1

	return xCol


def check_tile_collide_y(left, bottom, right, top):
	left_index = int((left + 1) // Tile.TILE_SIZE)
	bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
	right_index = int((right - 1) // Tile.TILE_SIZE)
	top_index = int(top // Tile.TILE_SIZE)

	yCol = False

	if bottom_index < 0:
		# Player dead or Bullet dead
		return None

	# y collide check here
	if server.tiles[bottom_index][left_index].get_is_collidable() or \
			server.tiles[bottom_index][right_index].get_is_collidable():
		yCol = -1
	elif (server.tiles[top_index][left_index].get_is_collidable() or \
		  server.tiles[top_index][right_index].get_is_collidable(True)):
		yCol = 1

	return yCol * (bottom_index + 1)


def enter():
	global current_stage, game_time, screen_offset
	current_stage += 1
	screen_offset = 0
	str = "어쨋든 스테이지 파일임_" + current_stage.__str__()

	game_time = 300
	global bullets
	bullets = []
	game_objects.load_objects_from_file(str)
	# now using test map
	test()


def restart():
	global current_stage
	current_stage -= 1
	game_objects.clear()
	enter()


def exit():
	game_objects.clear()
	pass


def handle_events():
	global game_coin, player_life, game_time
	server.gamePlayer.input()

	game_events = get_events()
	for event in game_events:
		if event.type == SDL_QUIT:
			game_framework.exit_program()

		elif event.type == SDL_KEYDOWN:
			if event.key == SDLK_ESCAPE:
				game_framework.exit_program()
			elif event.key == SDLK_MINUS:
				restart()
		# cheat keys
			# elif event.key == SDLK_F1:
			# 	server.gamePlayer.set_size(0)
			# elif event.key == SDLK_F2:
			# 	server.gamePlayer.set_size(1)
			# elif event.key == SDLK_F3:
			# 	server.gamePlayer.set_size(2)
			# elif event.key == SDLK_p:
			# 	game_coin += 10
			# elif event.key == SDLK_m:
			# 	player_life -= 1
			# elif event.key == SDLK_t:
			# 	game_time = 5


def update():
	global game_score, player_life, game_coin, game_time, screen_offset

	# move everything
	for objs in game_objects.all_objects():
		objs.update()

	# player-tile collide
	# check x col
	state = check_tile_collide_x(*(server.gamePlayer.get_position()))
	if state is not None:
		x_collide = state
		if x_collide:
			server.gamePlayer.go_x_back()
	# check y col
	state = check_tile_collide_y(*(server.gamePlayer.get_position()))
	if state is not None:
		y_collide = state
		if y_collide:
			if y_collide > 0:
				if server.gamePlayer.hit_ceil():
					l, b, r, t = server.gamePlayer.get_position()

					left_index = int((l + 1) // Tile.TILE_SIZE)
					right_index = int((r - 1) // Tile.TILE_SIZE)
					top_index = int(t // Tile.TILE_SIZE)

					server.tiles[top_index][left_index].collide()
					server.tiles[top_index][right_index].collide()
			else:
				server.gamePlayer.land(y_collide * Tile.TILE_SIZE * -1)
	else:
		print("player out")

	# bullets
	for bullet in bullets:
		state = check_tile_collide(*(bullet.get_position()))
		if state is not None:
			x_collide, y_collide = state
			if x_collide:
				game_objects.remove_object(bullet)
				bullets.remove(bullet)
				continue
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

	# server.monsters
	for monster in server.monsters:
		# player-monster collide
		if check_collide(monster, server.gamePlayer) and not server.gamePlayer.is_invincible():
			if not server.gamePlayer.size_down():
				# reload cur stage
				global player_life
				player_life -= 1
				if player_life < 0:
					# goto start state
					# exit cur state
					#
					game_framework.exit_program()
					return
				else:
					# reload cur state
					restart()
					return

		# monster-tile collide
		state = check_tile_collide(*(monster.get_position()))
		if state is not None:
			x_collide, y_collide = state
			if x_collide:
				monster.reverse()
			if y_collide:
				monster.land(y_collide * Tile.TILE_SIZE * -1)
		else:
			print("monster out")

		# monster-bullet collide
		for bullet in bullets:
			if check_collide(bullet, monster):
				game_objects.remove_object(bullet)
				game_objects.remove_object(monster)
				bullets.remove(bullet)
				server.monsters.remove(monster)
				game_score += 100
				continue

	# server.items
	for item in server.items:
		# kill lifetime end
		if not item.is_still_alive():
			game_objects.remove_object(item)
			server.items.remove(item)
			continue

		item_type = item.get_type()

		# check collide with player
		if check_collide(item, server.gamePlayer):
			if item_type == 0 or item_type == 3:
				# flower, mushroom(red)
				new_size = 1 + (item_type == 0)
				if new_size < server.gamePlayer.get_size():
					new_size = server.gamePlayer.get_size()
				server.gamePlayer.set_size(new_size)
				game_score += 500 + (item_type == 0) * 500
			elif item_type == 4:
				# green mushroom
				game_score += 500
				player_life += 1
			else:
				# star
				pass
			game_objects.remove_object(item)
			server.items.remove(item)
			continue

		# don't have to check col_tile
		if item_type == 2 or item_type == 0:
			continue

		# collide check if it is moving item
		state = check_tile_collide(*(item.get_position()))
		if state is not None:
			x_collide, y_collide = state
			if x_collide:
				item.reverse()
			if y_collide:
				item.land(y_collide * Tile.TILE_SIZE * -1)
		else:
			print("item out")

	if game_coin >= 100:
		player_life += 1
		game_coin -= 100
	game_time -= game_framework.frame_time
	if game_time <= 0:
		player_life -= 1
		restart()

	# screen offset setting
	screen_offset = clamp(0,
				   server.gamePlayer.get_x() - game_framework.w / 2,
				   len(server.tiles[0]) * Tile.TILE_SIZE - game_framework.w)



def draw():
	clear_canvas()
	for objs in game_objects.all_objects():
		objs.draw()

	# for line in server.tiles:
	# 	for t in line:
	# 		t.draw_breaking()

	font.draw(20, game_framework.h - 20,
			  'Score :' + str(game_score), (0, 0, 0))
	font.draw(150, game_framework.h - 20,
			  'Time :' + str(int(game_time)), (0, 0, 0))
	font.draw((game_framework.w - 80) / 2, game_framework.h - 20,
			  'Coin :' + str(game_coin), (0, 0, 0))
	font.draw(game_framework.w - 200, game_framework.h - 20,
			  'Stage :' + str(current_stage), (0, 0, 0))
	font.draw(game_framework.w - 100, game_framework.h - 20,
			  'Life :' + str(player_life), (0, 0, 0))
	# Life: ' + str(player_life)
	update_canvas()


def pause():
	pass


def resume():
	pass
