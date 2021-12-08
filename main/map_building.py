import pickle
# import os
# import Player
# import Tile
# import Monster
import Flag


def main():
	temp = Flag.Flag(400, 80)

	with open("checkpoint.sav", "wb") as f:
		pickle.dump(temp, f)
	pass


if __name__ == "__main__":
	main()
