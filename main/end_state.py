from pico2d import *
import game_framework
import GameWorld
import main_state
import world_build_state
import loading_state

import server
from Player import Player
import Tile
import Monster

name = "EndState"

screen = None
bgm = None
time = 0

def enter():
	global bgm, time, screen
	time = 0
	screen = load_image('resource/game_over.png')
	bgm = load_music('sound/game_over.mp3')
	bgm.play(1)



def exit():
	global bgm, screen
	del bgm
	del screen
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
		elif event.type == SDL_KEYDOWN:
			if event.key == SDLK_ESCAPE:
				game_framework.quit()
			else:
				game_framework.change_state(world_build_state)


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
			game_framework.change_state(world_build_state)


def draw():
	clear_canvas()
	screen.draw(get_canvas_width()//2, get_canvas_height()//2)
	update_canvas()
