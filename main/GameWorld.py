#

class GameObject:
	objects = [[], []]

	def add_object(obj, layer):
		objects[layer].append(obj)

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