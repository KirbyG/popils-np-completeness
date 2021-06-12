from game import Game
from common_constants import LEFT, DOWN, UP, RIGHT, ZERO, VARS_PER_CLAUSE

# popils-specific block color-coding
PLAYER = (255, 0, 0)  # red
LADDER = (0, 0, 255)  # blue
HARD = (210, 180, 140)  # tan
SOFT = (128, 128, 128)  # gray
PRINCESS = (250, 20, 200)  # pink
SUPPORT = (255, 255, 255)  # white

#popils-specific gadgets
SUB_GADGET_NEGATED = [LADDER, LADDER, SUPPORT, LADDER]
SUB_GADGET_ABSENT = [LADDER, SUPPORT, LADDER, SUPPORT]
SUB_GADGET_PRESENT = [SUPPORT, LADDER, LADDER, SUPPORT]
SUB_GADGETS = [SUB_GADGET_NEGATED, SUB_GADGET_ABSENT, SUB_GADGET_PRESENT]

# popils-specific gadget sizes
SUB_GADGET_HEIGHT = 4
GADGET_HEIGHT = 6

class Popils(Game):
    def __init__(self, puzzle):
        super(puzzle)

    def reduce(self, puzzle):
        #set dimensions of grid
        self.num_rows = 6 * (puzzle.num_clauses + 1)
        self.num_cols = 3 + (2 * puzzle.num_unique_vars)

        # Create bottom 3 rows & top 2 rows of puzzle
        # Remaining area, including frame, is made of HARD blocks
        grid = self.build_frame()

        #Place gadgets to construct puzzle
        self.build_clauses(grid, puzzle)
        
        return grid

    #reduce helpers
    def build_frame(self):
        player_row = player_col = 1
        assignment_row = 2
        transition_col = self.num_cols - 2  # Column with path (ladders) between areas
        # Initially set entire zone to indestructible blocks
        # Using this "*" notation twice doesn't produce expected results
        #   because Python just makes pointers to original tuple
        grid = [[HARD] * self.num_cols for row in range(self.num_rows)]

        # Starting zone
        grid[player_row][player_col] = PLAYER
        for i in range(player_col + 1, transition_col):
            grid[player_row][i] = SUPPORT
        grid[player_row][transition_col] = LADDER
        for i in range(player_col, transition_col - 1, 2):
            grid[assignment_row][i] = SOFT
        grid[assignment_row][transition_col] = LADDER

        # Ending zone
        grid[self.num_rows - 2][transition_col] = PRINCESS
        # Stop princess from walking
        grid[self.num_rows - 3][transition_col] = SOFT

        # Send back partially-built level
        return grid

    def build_clauses(self, grid, puzzle):
        row_pointer = 3

        for clause in range(puzzle.num_clauses):
            
            # Fill in gadget region for each variable for current tuple
            self.place_gadget(puzzle.expanded_form[clause], row_pointer)
            row_pointer += GADGET_HEIGHT

    def place_gadget(self, grid, variable_states, bottom_row):
        start_col = 2
        transition_col = self.num_cols - 2  # Column with path (ladders) between areas

        # Create transition to next zone
        grid[bottom_row][transition_col] = LADDER
        grid[bottom_row + 1][transition_col] = SUPPORT
        # state[bottom_row + 2][transition_col] is already HARD
        grid[bottom_row + 3][transition_col] = LADDER
        grid[bottom_row + 4][transition_col] = LADDER
        grid[bottom_row + 5][transition_col] = LADDER

        # Carve out walkable area, skipping gadget columns
        for i in range(start_col, transition_col, 2):
            grid[bottom_row + 1][i] = SUPPORT
            grid[bottom_row + 3][i] = SUPPORT
            grid[bottom_row + 4][i] = SUPPORT

        # Place ladders according to gadget structure
        for var_index in range(len(variable_states)):
            self.place_sub_gadget(
                variable_states[var_index], bottom_row + 1, 2 * var_index + 1)

    # Clone sub-gadget ladder structure

    def place_sub_gadget(self, grid, var_state, bottom_row, col):
        for i in range(SUB_GADGET_HEIGHT):
            grid[bottom_row + i][col] = SUB_GADGETS[var_state + 1][i]
    #end reduce helpers

    def generate_solution(self, puzzle):
        steps = []
        # set variables
        for truthiness in puzzle.solution:
            if truthiness == 1:
                steps.append(UP)
            steps.append(RIGHT)
            steps.append(RIGHT)
        # traverse level
        for clause in range(puzzle.num_clauses):
            steps.append(UP)
            steps.append(UP)
            steps.append(UP)

            satisfied = puzzle.satisfied_vars(puzzle.three_sat[clause], puzzle.solution)
            closest = max([abs(var) for var in satisfied])
            lateral_blocks = 2 * ( puzzle.num_vars + 1 - closest)

            # Move to nearest viable ladder
            for i in range(lateral_blocks):
                steps.append(LEFT)
            #climb to next clause
            steps.append(UP)
            steps.append(UP)
            #go back to the main ladder
            for i in range(lateral_blocks):
                steps.append(RIGHT)
            #get in position to traverse the next clause
            steps.append(UP)

        # Climb to princess
        steps.append(UP)
        steps.append(UP)
        steps.append(UP)

        return steps

    #command is one of the common vectors imported from common_constants
    def update(self, command):
        pass
    
    #update helpers
    def move(self, vector, player):
        pass

    def force(self, vector, player):
        pass
    #end update helpers

# If player walks off the top of a ladder, make them fall
# while (state[player.row - 1][player.col] == SUPPORT and player.occupying == SUPPORT):
#     game.force(DOWN, player)

# Change player's coordinates and refresh the displayed game grid
# def move(vector, player):
#     vertical = 0
#     horizontal = 1

#     state[player.row][player.col] = player.occupying
#     player.row += vector[vertical]
#     player.col += vector[horizontal]
#     player.occupying = state[player.row][player.col]
#     state[player.row][player.col] = PLAYER
#     draw(min(player.row, player.row - vector[vertical]), max(player.row, player.row - vector[vertical]),
#          min(player.col, player.col - vector[horizontal]), max(player.col, player.col - vector[horizontal]))

# # Wrapper for move() that enables auto-solving
# def force(vector, player):
#     global state
#     vertical = 0
#     horizontal = 1
#     target = state[player.row + vector[vertical]
#                    ][player.col + vector[horizontal]]
#     if vector == UP:
#         if target == SOFT:
#             for falling_row in range(player.row + 1, ROWS - 1):
#                 state[falling_row][player.col] = state[falling_row + 1][player.col]
#             state[ROWS - 1][player.col] = HARD
#             draw(player.row + 1, ROWS - 1, player.row, player.col)
#         elif player.occupying == LADDER and (target != HARD):
#             move(UP, player)
#     elif target != HARD:
#         move(vector, player)
# 
