#

# layer 0 : tiles
# layer 1 : coins, items
# layer 2 : monster
# layer 3 : player
# layer 4 : ui??

class GameObject:
	objects = [[], [], [], [], []]

	@classmethod
	def add_object(obj, layer):
		objects[layer].append(obj)

	@classmethod
	def remove_object(o):
		for i in range(len(objects)):
			if o in objects[i]:
				objects[i].remove(o)
				del o
				break

	@classmethod
	def clear():
		for o in all_objects():
			del o
		for l in objects:
			l.clear()

	@classmethod
	def all_objects():
		for i in range(len(objects)):
			for o in objects[i]:
				yield o
