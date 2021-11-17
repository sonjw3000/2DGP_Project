import time

w, h = 800, 600

gameLoop = True
frame_time = 0.0
stack = None


def exit_program():
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
