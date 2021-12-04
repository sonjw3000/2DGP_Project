import random
import json
import pickle
import os

from pico2d import *
import game_framework
import GameWorld
import main_state
import server
import Player
import Tile
import Monster


boy = None


name = "WorldBuildState"

menu = None

def enter():
    global menu
    menu = load_image('menu.png')
    hide_cursor()
    hide_lattice()

def exit():
    global menu
    del menu

def pause():
    pass

def resume():
    pass


# make new game
def create_new_world():
    server.gamePlayer = Player.Player(50, 80, 0)
    GameWorld.add_object(server.gamePlayer, 1)

    # new stage0 tile
    with open("zombie_data.json", 'r') as f:
        zombie_data_list = json.load(f)

    # new stage0 monster
    for data in zombie_data_list:
        zombie = Zombie(data['name'], data['x'], data['y'], data['size'])
        GameWorld.add_object(zombie, 1)


# load last game
def load_saved_world():
    GameWorld.load()

    for o in game_world.all_objects():
        if isinstance(o, Boy):
            server.boy = o
            break

    pass



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            create_new_world()
            game_framework.change_state(main_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            load_saved_world()
            game_framework.change_state(main_state)

def update():
    pass

def draw():
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()






