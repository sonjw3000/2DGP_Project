from pico2d import *
# from pynput import keyboard
# import keyboard
import Player
import Tile
import Bullet
import Monster


# All rectangle have left, bottom position as their offset

def rect_col_check(rt1, rt2):
	rl, rb, rr, rt = rt1
	ll, lb, lr, lt = rt2
	return rl <= lr and rr >= ll and rt >= lb and rb <= lt


class GameRunner:
	def __init__(self):
		# init game here
		self.bGameLoop = True
		self.max_x_index = 20

		# Game Objects
		self.mario = Player.Player(80, 80, 2)
		self.tiles = [Tile.Tile(0, 0, True, True, 0)]
		self.monsters = []
		self.bullets = []

	# Constructor end

	def __handle_events(self):
		game_events = get_events()
		for event in game_events:
			if event.type == SDL_QUIT:
				self.bGameLoop = False
			elif event.type == SDL_KEYDOWN:
				if event.key == SDLK_ESCAPE:
					self.bGameLoop = False

	# Event handler End

	def input(self):
		self.__handle_events()
		pos = self.mario.input()
		if pos != None:
			x, y = pos
			bullet = Bullet.Bullet(x, y, self.mario.get_dir())
			self.bullets.append(bullet)

	# Input End
	def __collide_check_with_tile(self, left, bottom, right, top, is_mario=False):
		left_index = int((left - 1) // Tile.TILE_SIZE)
		bottom_index = int((bottom - 1) // Tile.TILE_SIZE)
		right_index = int(right // Tile.TILE_SIZE)
		top_index = int(top // Tile.TILE_SIZE)

		xCol = False
		yCol = False

		# x collide check here
		if left_index < 0:
			xCol = True
			left_index = 0
		elif right_index >= self.max_x_index:
			xCol = True
			right_index = self.max_x_index - 1
		elif self.tiles[bottom_index + 1][left_index].get_is_collidable() or \
				self.tiles[top_index][left_index].get_is_collidable():
			xCol = True
		elif self.tiles[bottom_index + 1][right_index].get_is_collidable() or \
				self.tiles[top_index][right_index].get_is_collidable():
			xCol = True

		# y collide check here
		if bottom_index < 0:
			# Player dead or Bullet dead
			return None
		elif self.tiles[bottom_index][left_index].get_is_collidable() or \
				self.tiles[bottom_index][right_index].get_is_collidable():
			yCol = True
		elif (self.tiles[top_index][left_index].get_is_collidable(True) or \
			  self.tiles[top_index][right_index].get_is_collidable(True)) and is_mario:
			# hit bottom of the box
			# * -1 jump speed
			if self.mario.hit_ceil():
				# break tile
				self.tiles[int(top_index)][int(left_index)].collide()
				self.tiles[int(top_index)][int(right_index)].collide()

		return xCol, yCol * (bottom_index + 1)

	# def __collide_check(self):
	# 	# collide check here
	# 	bLand = False
	# 	xCol = False
	# 	l, b, r, t = self.mario.get_position()
	#
	# 	left_index = int((l - 1) // Tile.TILE_SIZE)
	# 	bottom_index = int((b - 1) // Tile.TILE_SIZE)
	# 	right_index = int(r // Tile.TILE_SIZE)
	# 	top_index = int(t // Tile.TILE_SIZE)
	#
	# 	# Check X block
	# 	# Right with block
	# 	if left_index < 0:
	# 		xCol = self.mario.go_x_back()
	# 		left_index = 0
	# 	elif right_index >= self.max_x_index:
	# 		xCol = self.mario.go_x_back()
	# 		right_index = self.max_x_index - 1
	# 	elif self.tiles[bottom_index + 1][left_index].get_is_collidable() or \
	# 			self.tiles[top_index][left_index].get_is_collidable():
	# 		xCol = self.mario.go_x_back()
	# 	elif self.tiles[bottom_index + 1][right_index].get_is_collidable() or \
	# 			self.tiles[top_index][right_index].get_is_collidable():
	# 		xCol = self.mario.go_x_back()
	#
	# 	# Falling Check
	# 	# Check Y axis Collide
	# 	if bottom_index < 0:
	# 		# PlayerDead
	# 		pass
	# 	elif self.tiles[bottom_index][left_index].get_is_collidable() or \
	# 			self.tiles[bottom_index][right_index].get_is_collidable():
	# 		bLand = True
	# 	elif self.tiles[top_index][left_index].get_is_collidable(True) or \
	# 			self.tiles[top_index][right_index].get_is_collidable(True):
	# 		# hit bottom of the box
	# 		# * -1 jump speed
	# 		if self.mario.hit_ceil():
	# 			# break tile
	# 			self.tiles[int(top_index)][int(left_index)].collide()
	# 			self.tiles[int(top_index)][int(right_index)].collide()
	#
	# 	# Monster Y Check
	# 	# pass
	#
	# 	return (bLand * Tile.TILE_SIZE * (bottom_index + 1)), xCol


	def update(self, delta_time=1):
		dt = get_time()
		# Player and Tile collide check
		l, b, r, t = self.mario.get_position()
		result = self.__collide_check_with_tile(l, b, r, t, True)
		if result != None:
			xCol, yCol = result
		else:
			# Player Dead if out of range
			return
		if xCol:
			self.mario.go_x_back()

		# Bullet and Tile collide check and move
		for bullet in self.bullets:
			l, b, r, t = bullet.get_position()
			result = self.__collide_check_with_tile(l, b, r, t)
			if result != None:
				bullet_xCol, bullet_yCol = result
			else:
				self.bullets.remove(bullet)
				continue
			if bullet_xCol:
				self.bullets.remove(bullet)
				continue
			if not bullet.update(bullet_yCol):
				self.bullets.remove(bullet)

		# Monster
		for monster in self.monsters:
			l, b, r, t = monster.get_position()

			# col check with player
			# if mon die? pop this
			# else break game

			# collide with bullets
			for bullet in self.bullets:
				bul_rect = bullet.get_position()
				if self.rect_col_check(bul_rect, (l, b, r, t)):
					self.monsters.remove(monster)
					continue

			# tiles
			result = self.__collide_check_with_tile(l, b, r, t, False)




			if result != None:
				Monster_xCol, monster_yCol = result
			else:
				# Monster Dead, monster out of range
				# delete this monster
				continue
				pass
			if Monster_xCol:
				monster.reverse()
				monster.update(monster_yCol * Tile.TILE_SIZE)





		# Tile Update
		for line in self.tiles:
			for t in line:
				t.update()

		self.mario.move(yCol * Tile.TILE_SIZE, dt)

	# Update End

	def draw(self):
		clear_canvas()

		for line in self.tiles:
			for t in line:
				t.draw()

		for line in self.tiles:
			for t in line:
				t.draw_breaking()

		for bullet in self.bullets:
			bullet.draw()

		for monster in self.monsters:
			monster.draw()

		self.mario.draw()
		update_canvas()

	# Draw End

	def init_game(self):
		bullet_img = load_image('./resource/bullets.png')
		tileImage = load_image('./resource/tiles/overworld.png')
		monsterImage = load_image('./resource/monsters.png')

		Tile.Tile.set_image(tileImage)
		Bullet.Bullet.set_image(bullet_img)
		Monster.Monster.set_image(monsterImage)


# Class End


def main():
	# Init game Settings
	open_canvas()
	game = GameRunner()

	# Game Loop
	while game.bGameLoop:
		game.input()
		game.update()
		game.draw()
		delay(0.01)

	close_canvas()


if __name__ == "__main__":
	main()
