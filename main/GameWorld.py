#
import os
import pickle
import server
# layer 0 : tiles
# layer 1 : coins, items
# layer 2 : monster
# layer 3 : player
# layer 4 : ui??

objects = [[], [], [], [], []]


def add_object(obj, layer):
	objects[layer].append(obj)


def add_objects(new_list, layer):
	objects[layer] += new_list


def remove_object(o):
	for i in range(len(objects)):
		if o in objects[i]:
			objects[i].remove(o)
			del o
			break


def clear():
	for o in all_objects():
		del o
	for l in objects:
		l.clear()


def all_objects():
	for i in range(len(objects)):
		for o in objects[i]:
			yield o


# Tile : 0 // Coin, Item : 1 // Monster : 2 // Player : 3
def get_objects_from_layer(layer_index):
	return objects[layer_index]


def load_objects_from_file(file_route):
	pass


def save():
	# with open('game.sav', 'wb') as f:
	# 	pickle.dump(objects, f)
	with open("tiles.sav", "wb") as f:
		pickle.dump(server.tiles, f)

	with open("monsters.sav", "wb") as f:
		pickle.dump(objects[2], f)

	with open("player.sav", "wb") as f:
		pickle.dump(objects[3], f)


def load():
	global objects

	clear()
	# move to save directory

	# load tiles
	with open("tiles.sav", "rb") as f:
		tiles = pickle.load(f)
		for tile in tiles:
			add_objects(tile, 0)
		server.tiles = tiles

	with open("monsters.sav", "rb") as f:
		monster = pickle.load(f)
		objects[2] = monster
		server.monsters = monster

	with open("player.sav", "rb") as f:
		player = pickle.load(f)
		objects[3] = player
		server.gamePlayer = player
