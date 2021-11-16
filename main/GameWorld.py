#

# layer 0 : tiles
# layer 1 : coins, items
# layer 2 : monster
# layer 3 : player
# layer 4 : ui??

class GameObjects:
	def __init__(self):
		self.objects = [[], [], [], [], []]

	def add_object(self, obj, layer):
		self.objects[layer].append(obj)

	def remove_object(self, o):
		for i in range(len(self.objects)):
			if o in self.objects[i]:
				self.objects[i].remove(o)
				del o
				break

	def clear(self):
		for o in self.all_objects():
			del o
		for l in self.objects:
			l.clear()

	def all_objects(self):
		for i in range(len(self.objects)):
			for o in self.objects[i]:
				yield o

	# Tile : 0 // Coin, Item : 1 // Monster : 2 // Player : 3
	def get_objects_from_layer(self, layer_index):
		return self.objects[layer_index]

	def load_objects_from_file(self, file_route):
		pass
