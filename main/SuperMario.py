from pico2d import *
import game_framework

import main_state

open_canvas(game_framework.w, game_framework.h)
game_framework.run(main_state)
close_canvas()