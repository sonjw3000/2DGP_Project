import time
from pico2d import *

w, h = 800, 600

gameLoop = True
frame_time = 0.0
stack = None

coin_bgm = None
jump_bgm = None
item_init_bgm = None
power_up_bgm = None
size_down_bgm = None
breaking_bgm = None
monster_dead_bgm = None
fire_ball_bgm = None

class GameState:
	def __init__(self, state):
		self.enter = state.enter
		self.exit = state.exit
		self.pause = state.pause
		self.resume = state.resume
		self.handle_events = state.handle_events
		self.update = state.update
		self.draw = state.draw


def exit_program():
	global gameLoop
	gameLoop = False


def change_state(state):
	global stack
	if (len(stack) > 0):
		# execute the current state's exit function
		stack[-1].exit()
		# remove the current state
		stack.pop()
	stack.append(state)
	state.enter()


def push_state(state):
	global stack
	if (len(stack) > 0):
		stack[-1].pause()
	stack.append(state)
	state.enter()


def pop_state():
	global stack
	if (len(stack) > 0):
		# execute the current state's exit function
		stack[-1].exit()
		# remove the current state
		stack.pop()

	# execute resume function of the previous state
	if (len(stack) > 0):
		stack[-1].resume()


def quit():
	global gameLoop
	gameLoop = False


def run(start_state):
	global coin_bgm, jump_bgm, item_init_bgm, power_up_bgm, monster_dead_bgm
	global size_down_bgm, breaking_bgm, fire_ball_bgm
	coin_bgm = load_wav('sound/effect/coin.wav')
	coin_bgm.set_volume(10)
	jump_bgm = load_wav('sound/effect/jump.wav')
	jump_bgm.set_volume(20)
	item_init_bgm = load_wav('sound/effect/item_init.wav')
	item_init_bgm.set_volume(40)
	power_up_bgm = load_wav('sound/effect/power_up.wav')
	power_up_bgm.set_volume(40)

	size_down_bgm = load_wav('sound/effect/size_down.wav')
	size_down_bgm.set_volume(40)
	breaking_bgm = load_wav('sound/effect/breaking.wav')
	breaking_bgm.set_volume(20)

	fire_ball_bgm = load_wav('sound/effect/fire_ball.wav')
	fire_ball_bgm.set_volume(20)
	monster_dead_bgm = load_wav('sound/effect/monster_dead.wav')
	power_up_bgm.set_volume(40)

	global gameLoop, stack, frame_time
	stack = [start_state]
	start_state.enter()

	cur_time = time.time()

	while gameLoop:
		stack[-1].handle_events()
		stack[-1].update()
		stack[-1].draw()

		frame_time = time.time() - cur_time
		cur_time += frame_time

		if frame_time >= 0.2:
			frame_time = 0.2

	while (len(stack) > 0):
		stack[-1].exit()
		stack.pop()
