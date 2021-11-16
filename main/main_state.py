from GameWorld import *
from pico2d import *
import Player
import Bullet
import Tile

# for test
import TestMap

game_objects = GameObjects()


def test():
	global  game_objects
	# Tiles
	for i in range(15):
		for j in range(20):
		game_objects.add_object(TestMap.TestMap[i][j], 0)

	# Monsters
	for i in TestMap.Monster:
		game_objects.add_object(i, 2)

	# Player
	game_objects.add_object(Player.Player(),3)

def enter():
	# game_objects.load_objects_from_file("")
	test()

def exit():
	pass

def handle_events():
	game_objects.get_objects_from_layer(3)[0].input()

	game_events = get_events()
	for event in game_events:
		if event.type == SDL_QUIT:
			# self.bGameLoop = False
			# should change state to title
			pass
		elif event.type == SDL_KEYDOWN:
			if event.key == SDLK_ESCAPE:
				# self.bGameLoop = False
				# should change state to title
				pass

def update():
	for objs in game_objects.all_objects():
		objs.update()


def draw():
	clear_canvas()
	for objs in game_objects.all_objects():
		objs.draw()
	update_canvas()


def pause():
	pass


def resume():
	pass
