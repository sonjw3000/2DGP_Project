from pico2d import *
import Player
import Monster
import Bullet
import Tile
import Flag
import game_framework
import GameWorld
import copy

import world_build_state
import dead_state
import goal_state

import server

# for test
# import TestMap

font = None
bgm = None

current_stage = 0

# game var
player_life = 5
game_score = 0
game_coin = 0
game_time = 300

screen_offset = 0


def set_images():
	tileImage = load_image('./resource/tiles/overworld.png')
	Tile.Tile.set_image(tileImage)

	bulletImg = load_image('./resource/bullets.png')
	Bullet.Bullet.set_image(bulletImg)

	monsterImg = load_image("./resource/monsters.png")
	Monster.Monster.set_image(monsterImg)

	playerImg = load_image("./resource/Mario_Real.png")
	Player.Player.set_image(playerImg)

	flagImage = load_image('./resource/flag.png')
	Flag.Flag.set_image(flagImage)

	global font
	font = load_font('./resource/ENCR10B.TTF', 16)

	global bgm
	bgm = load_music('./sound/main_them.mp3')
	bgm.repeat_play()
	bgm.set_volume(20)


# def test():
# 	# Tiles
#
# 	server.tiles = []
# 	for lists in TestMap.TestMapTile:
# 		server.tiles.append(lists)
#
# 	for i in range(len(server.tiles) - 1, 0 - 1, -1):
# 		GameWorld.add_objects(server.tiles[i][::-1], 0)
#
# 	# Monsters
# 	server.monsters = []
# 	for lists in TestMap.Monster:
# 		server.monsters.append(lists)
#
# 	GameWorld.add_objects(server.monsters, 2)
#
# 	# Player
# 	server.gamePlayer = Player.Player(50, 80, 0)
# 	GameWorld.add_object(server.gamePlayer, 3)
#
# 	# item
# 	server.items = []
#
# 	# load img
# 	tileImage = load_image('./resource/tiles/overworld.png')
# 	Tile.Tile.set_image(tileImage)
#
# 	bulletImg = load_image('./resource/bullets.png')
# 	Bullet.Bullet.set_image(bulletImg)
#
# 	monsterImg = load_image("./resource/monsters.png")
# 	Monster.Monster.set_image(monsterImg)
#
# 	flagImage = load_image('./resource/tiles/flag.png')
# 	Flag.Flag.set_image(flagImage)
#
# 	global font
# 	font = load_font('./resource/ENCR10B.TTF', 16)


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
	if bottom_index + 1 >= len(server.tiles):
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
	if top_index >= len(server.tiles):
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
	if top_index >= len(server.tiles):
		return None

	# y collide check here
	if left_index < 0:
		left_index = 0
	elif right_index >= len(server.tiles[0]):
		right_index = len(server.tiles[0]) - 1

	if server.tiles[bottom_index][left_index].get_is_collidable() or \
			server.tiles[bottom_index][right_index].get_is_collidable():
		yCol = -1
	elif (server.tiles[top_index][left_index].get_is_collidable() or \
		  server.tiles[top_index][right_index].get_is_collidable(True)):
		yCol = 1

	return yCol * (bottom_index + 1)


def enter():
	global game_time, screen_offset
	screen_offset = 0

	# GameWorld.load(current_stage)
	server.bullets = []
	server.items = []
	# game_time = 300

	# now using test map
	# test()
	set_images()


def restart():
	# global game_time
	# game_time = 300

	# server.items.clear()

	# GameWorld.clear()
	# if server.checkpoint.bCaptured:
	# 	GameWorld.load(-3)
	# else:
	# 	GameWorld.load(current_stage)
	game_framework.change_state(dead_state)


def exit():
	# GameWorld.clear()
	global bgm
	bgm.stop()
	del bgm
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
			elif event.key == SDLK_s:
				print("Game Save!")
				GameWorld.save()
			# GameWorld.save()
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
	for objs in GameWorld.all_objects():
		objs.update()

	# player-tile collide

	# check x col
	state = check_tile_collide_x(*(server.gamePlayer.get_position()))
	if state is not None:
		x_collide = state
		if x_collide:
			l, b, r, t = server.gamePlayer.get_position()

			left_index = int((l + 1) // Tile.TILE_SIZE)
			right_index = int((r - 1) // Tile.TILE_SIZE)
			top_index = int(t // Tile.TILE_SIZE)

			if server.tiles[top_index][left_index].is_goal() or \
					server.tiles[top_index][right_index].is_goal():
				game_framework.change_state(goal_state)
				return

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

					if server.tiles[top_index][left_index].is_goal() or \
							server.tiles[top_index][right_index].is_goal():
						game_framework.change_state(goal_state)
						return

					server.tiles[top_index][left_index].collide()
					server.tiles[top_index][right_index].collide()
			else:
				server.gamePlayer.land(y_collide * Tile.TILE_SIZE * -1)
	else:
		print("player out")

	# bullets
	for bullet in server.bullets:
		state = check_tile_collide(*(bullet.get_position()))
		if state is not None:
			x_collide, y_collide = state
			if x_collide:
				GameWorld.remove_object(bullet)
				server.bullets.remove(bullet)
				continue
			if y_collide:
				bullet.hit_floor()
		else:
			GameWorld.remove_object(bullet)
			server.bullets.remove(bullet)
			continue

		# bullet timer
		if not bullet.is_still_alive():
			GameWorld.remove_object(bullet)
			server.bullets.remove(bullet)

	# server.monsters
	for monster in server.monsters:
		if monster.bDead:
			if monster.life_dead():
				GameWorld.remove_object(monster)
				server.monsters.remove(monster)
			continue

		# player-monster collide
		if check_collide(monster, server.gamePlayer) and not server.gamePlayer.is_invincible():
			monster_rect = monster.get_position()
			player_rect = server.gamePlayer.get_position()

			dx = monster_rect[2] - player_rect[0]
			if dx > Player.PLAYER_SIZE:
				dx = player_rect[2] - monster_rect[0]
			dy = monster_rect[3] - player_rect[1]
			if dx < dy:
				server.gamePlayer.size_down()
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
			else:
				monster.go_dead(False)
				game_framework.monster_dead_bgm.play(1)
				server.gamePlayer.bounce()
				continue

		# monster-tile collide
		state = check_tile_collide(*(monster.get_position()))
		if state is not None and not monster.bDead:
			x_collide, y_collide = state
			if x_collide:
				monster.reverse()
			if y_collide:
				monster.land(y_collide * Tile.TILE_SIZE * -1)
		else:
			print("monster out")

		# monster-bullet collide
		for bullet in server.bullets:
			if check_collide(bullet, monster):
				GameWorld.remove_object(bullet)
				server.bullets.remove(bullet)
				monster.go_dead(True)
				game_framework.monster_dead_bgm.play(1)
				game_score += 100
				continue



	# server.items
	for item in server.items:
		# kill lifetime end
		if not item.is_still_alive():
			GameWorld.remove_object(item)
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
			GameWorld.remove_object(item)
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

	# server.checkpoint
	if check_collide(server.checkpoint, server.gamePlayer):
		server.checkpoint.get_hit()

	if game_coin >= 100:
		player_life += 1
		game_coin -= 100
	game_time -= game_framework.frame_time
	if game_time <= 0:
		player_life -= 1
		restart()

	if player_life <= 0:
		print("Game Over")
		game_framework.change_state(world_build_state)

	# screen offset setting
	screen_offset = clamp(0,
						  server.gamePlayer.get_x() - game_framework.w / 2,
						  len(server.tiles[0]) * Tile.TILE_SIZE - game_framework.w)


def draw():
	clear_canvas()
	for objs in GameWorld.all_objects():
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
