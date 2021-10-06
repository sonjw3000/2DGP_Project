from pico2d import *
#from pynput import keyboard
import keyboard
import Player
# All rectangle have left, bottom position as their offset



def handleEvents():
	global bGameLoop

	events = get_events()
	for event in events:
		if event.type == SDL_QUIT: 			bGameLoop = False
		elif event.type == SDL_KEYDOWN:
			## Player Move
			#if event.key == SDLK_RIGHT:		mario.addDir(1)
			#elif event.key == SDLK_LEFT:	mario.addDir(-1)
			# Quit
			#el
			if event.key == SDLK_ESCAPE:	bGameLoop = False
			# test
			elif event.key == SDLK_F1:		mario.spriteUp()
			elif event.key == SDLK_F2:		mario.spriteDown()
			elif event.key == SDLK_F3:		mario.sizeUp()
			elif event.key == SDLK_F4:		mario.sizeDown()
		#elif event.type == SDL_KEYUP:
		#	# Player Move
		#	if event.key == SDLK_RIGHT:		mario.addDir(-1)
		#	elif event.key == SDLK_LEFT:	mario.addDir(1)



def input():
	handleEvents()
	mario.input()

def update():
	global mario
	mario.move()

def draw():
	clear_canvas()

	mario.draw()
	update_canvas()


# Init game Settings
open_canvas()

mario = Player.Player()
bGameLoop = True


# Game Loop
while(bGameLoop):

	input()
	update()
	draw()


	delay(0.01)



close_canvas()