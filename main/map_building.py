import pickle
# import os
# import Player
from Tile import *

# import Monster
# import Flag

T = TILE_SIZE


def main():
	# temp = Tile.tile(400, 80)

	# TestMapTile = [
	# 	[[Tile(T * i, T * 0, True, False, 0) for i in range(40)] + [Tile(T * i, T * 0, True, False, 0) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 1, False + (i == 19 or i == 14), False, 56 - 56 * (i == 19 or i == 14)) for i in range(40)] + [Tile(T * i, T * 1, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 2, False, False, 56) for i in range(40)] + [Tile(T * i, T * 2, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 3, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 4, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 5, True, True, 33) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 6, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 7, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 8, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 9, False, False, 56, (i // 10) * 4) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 10, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 11, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 12, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 13, True, True, 33 + 31 * (i >= 10), 3) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# 	[[Tile(T * i, T * 14, False, False, 56) for i in range(40)] + [Tile(T * i, T * 3, True, False, i == 40 * 85) for i in range(40, 43)]],
	# ]

	TestMapTile = [
		[Tile(TILE_SIZE * i, TILE_SIZE * 0, True, False, 0) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 1, False + (i == 19 or i == 14), False, 56 - 56 * (i == 19 or i == 14)) for i
		 in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 2, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 3, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 4, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 5, True, True, 33) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 6, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 7, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 8, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 9, False, False, 56, (i // 10) * 4) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 10, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 11, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 12, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 13, False, False, 56) for i in range(40)],
		[Tile(TILE_SIZE * i, TILE_SIZE * 14, False, False, 56) for i in range(40)],
	]

	for i in range(len(TestMapTile)):
		if i == 0:
			TestMapTile[i] += [Tile(T * j, T * i, True, False, 0) for j in range(40, 43)]
		elif i <= 10:
			TestMapTile[i] += [Tile(T * 40, T * i, True, False, 85)] + [Tile(T * j, T * i, False, False, 56) for j in range(41, 43)]
		elif i == 11:
			TestMapTile[i] += [Tile(T * 40, T * i, True, False, 101)] + [Tile(T * j, T * i, False, False, 56) for j in range(41, 43)]
		else:
			TestMapTile[i] += [Tile(T * j, T * i, False, False, 56) for j in range(40, 43)]

	# TestMapTile = TestMapTile[::-1]

	with open("tiles.sav", "wb") as f:
		pickle.dump(TestMapTile, f)
	pass


if __name__ == "__main__":
	main()
