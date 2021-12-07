#
import os
import pickle
import server
import json
import main_state

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

	cur_path = os.getcwd()
	# print(cur_path)
	os.chdir(os.path.join(cur_path, 'stage/lastgame'))

	# scene num
	with open("scene_data.json", 'w') as f:
		data = {
			"life": main_state.player_life,
			"score": main_state.game_score,
			"coin": main_state.game_coin,
			"time": main_state.game_time,
			"stage": main_state.current_stage
		}
		json.dump(data, f)

	# tiles
	with open("tiles.sav", "wb") as f:
		pickle.dump(server.tiles, f)

	# monsters
	with open("monsters.sav", "wb") as f:
		pickle.dump(objects[2], f)

	# player
	with open("player.sav", "wb") as f:
		pickle.dump(server.gamePlayer, f)

	os.chdir(cur_path)


def load(stage_num):
	global objects

	main_state.current_stage = stage_num
	clear()
	# move to save directory
	cur_path = os.getcwd()
	# print(cur_path)
	if stage_num == -1:			# this is test map
		os.chdir(os.path.join(cur_path, 'stage/test'))
		pass
	elif stage_num == -2:		# load last saved game
		os.chdir(os.path.join(cur_path, 'stage/lastgame'))
		with open("scene_data.json", 'r') as f:
			stage_data = json.load(f)
			main_state.player_life = stage_data["life"]
			main_state.game_score = stage_data["score"]
			main_state.game_coin = stage_data["coin"]
			main_state.game_time = stage_data["time"]
			main_state.current_stage = stage_data["stage"]


	# load tiles
	with open("tiles.sav", "rb") as f:
		tiles = pickle.load(f)
		for tile in tiles:
			add_objects(tile, 0)
		server.tiles = tiles

	with open("monsters.sav", "rb") as f:
		monster = pickle.load(f)
		add_objects(monster, 2)
		server.monsters = monster

	with open("player.sav", "rb") as f:
		player = pickle.load(f)
		add_object(player, 3)
		server.gamePlayer = player

	os.chdir(cur_path)

	print("stage :", stage_num, "load completed")
