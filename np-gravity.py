# this file reads user input, first from CLI, then in the game loop

# SETUP

import argparse
import pygame
# from pathlib import Path
from puzzle import Puzzle
from popils import Popils
from megalit import Megalit
from artist import Artist
from common_constants import LEFT, RIGHT, DOWN, UP, ZERO, Vector

# default 3SAT instance. Will be ignored if user provides alternative
DEFAULT_3SAT = "examples/default.cnf"


# handle input from the command line
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='filename',
                        help="file containing an instance of 3SAT in DIMACS CNF format")
    parser.add_argument('-s', dest='solver', action='store_true',
                        help='run puzzle auto-solver')
    parser.add_argument('-m', '--megalit', action='store_true',
                        help='reduce 3SAT to Megalit instead of Popils')
    return parser.parse_args()


# add line break after pygame importing output
print()

# read in 3SAT problem
args = parse_arguments()

# set raw instance input data from command line or file
filepath = args.filename if args.filename else DEFAULT_3SAT

# create game instance of the correct type
puzzle = Puzzle(filepath)
game = Megalit(puzzle) if args.megalit else Popils(puzzle)
artist = Artist(game)
# game loop
while not game.complete:
    # update gamestate
    if args.solver:  # autosolver mode
        game.update(game.solution[game.solution_step])
        game.solution_step += 1
        if game.solution_step == len(game.solution):
            game.complete = True
        for event in pygame.event.get():
            pass
    else:  # user input mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.complete = True
            elif event.type == pygame.KEYUP:  # pass basic directional inputs to game
                if event.key == pygame.K_LEFT:
                    game.update(LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.update(RIGHT)
                elif event.key == pygame.K_UP:
                    game.update(UP)
                elif event.key == pygame.K_DOWN:
                    game.update(DOWN)
                elif event.key == pygame.K_SPACE:
                    game.update(ZERO)
    # iterate game display with framerate capped at 15 FPS
    artist.draw()
    artist.clock.tick(60)