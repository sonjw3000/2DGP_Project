from pico2d import *
import game_framework
import GameWorld
import main_state
import world_build_state

import server
from Player import Player
import Tile
import Monster

current_stage = 0

name = "LoadingState"

screen = None
font = None

time = 0

def enter():
	global screen, font
	screen = load_image("./resource/load_screen.png")
	font = load_font('./resource/ENCR10B.TTF', 32)

def exit():
	global time, screen, font
	time = 0
	del screen
	del font


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

	# screen time 1.5 sec
	if time >= 1.5:
		game_framework.change_state(main_state)
	pass

def draw():
	clear_canvas()
	screen.draw(get_canvas_width() // 2, get_canvas_height() // 2)
	font.draw(get_canvas_width() // 2 + 20, get_canvas_height() // 2 + 100,
			  str(main_state.current_stage), (255, 255, 255))
	font.draw(get_canvas_width() // 2 + 15, get_canvas_height() // 2 + 10,
			  str(main_state.player_life), (255, 255, 255))
	update_canvas()
