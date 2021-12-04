import time

w, h = 800, 600

gameLoop = True
frame_time = 0.0
stack = None


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
