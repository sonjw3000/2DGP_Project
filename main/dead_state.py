from pico2d import *
import game_framework
import GameWorld
import main_state
import world_build_state
import loading_state
import end_state

import server
from Player import Player
import Tile
import Monster

name = "DeadState"

menu = None
bgm = None
time = 0

def enter():
	global bgm, time
	time = 0
	bgm = load_music('sound/1_down.mp3')
	bgm.play(1)
	server.gamePlayer.dead()


def exit():
	global bgm
	del bgm
	pass


def pause():
	pass


def resume():
	pass


def handle_events():
	events = get_events()
	for event in events:
		if event.type == SDL_QUIT:
			game_framework.quit()
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			game_framework.quit()


def update():
	global time

	time += game_framework.frame_time

	server.gamePlayer.dead_update()

	if time >= 4:
		if main_state.player_life > 0:
			if server.checkpoint.bCaptured:
				GameWorld.load(-3)
			else:
				GameWorld.load(main_state.current_stage)

			main_state.game_time = 300
			game_framework.change_state(loading_state)
			return
		else:
			game_framework.change_state(end_state)


def draw():
	clear_canvas()
	for objs in GameWorld.all_objects():
		if objs is Player:
			print("HELLO PLAYER")
		objs.draw()

	# for line in server.tiles:
	# 	for t in line:
	# 		t.draw_breaking()

	main_state.font.draw(20, game_framework.h - 20,
						 'Score :' + str(main_state.game_score), (0, 0, 0))
	main_state.font.draw(150, game_framework.h - 20,
						 'Time :' + str(int(main_state.game_time)), (0, 0, 0))
	main_state.font.draw((game_framework.w - 80) / 2, game_framework.h - 20,
						 'Coin :' + str(main_state.game_coin), (0, 0, 0))
	main_state.font.draw(game_framework.w - 200, game_framework.h - 20,
						 'Stage :' + str(main_state.current_stage), (0, 0, 0))
	main_state.font.draw(game_framework.w - 100, game_framework.h - 20,
						 'Life :' + str(main_state.player_life), (0, 0, 0))
	# Life: ' + str(player_life)
	update_canvas()
