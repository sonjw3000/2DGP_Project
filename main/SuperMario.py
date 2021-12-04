from pico2d import *
import game_framework

import world_build_state
import main_state

open_canvas(game_framework.w, game_framework.h)
game_framework.run(world_build_state)
close_canvas()