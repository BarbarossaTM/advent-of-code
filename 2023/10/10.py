#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 11 Dec 2023 11:44:23 PM CET
#

import sys

# The pipes are arranged in a two-dimensional grid of tiles:
#
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
#
grid = [
    # [ { 'sym': <sym>, 'dist:' <int> } ... ]
    # ...
]

# same dimensions as grid, used to store distance computations
grid_dist = []

# Start position, to be filled by parse_file()
S = [0, 0]

move_map = {
    # <symbol> : { <previous move>: <next move> },
    # | + - => repeat previous action
    '7' : {
        'right': 'down',
        'up': 'left',
    },
    'J' : {
        'down': 'left',
        'right': 'up'
    },
    'L' : {
        'left': 'up',
        'down': 'right'
    },
    'F' : {
        'up' :'right',
        'left' : 'down',
    },
}

move_to_steps = {
    'up'   : [-1, 0],
    'right': [0, 1],
    'down' : [1, 0],
    'left' : [0, -1],
}

line_len = 0

def parse_file(file_fh) -> None:
    global line_len
    grid_dist_line = []

    S_found = False

    for line in file_fh:
        if not line_len:
            line_len = len(line)
            grid_dist_line = [0 for i in range(line_len)]

        grid.append(list(line))
        grid_dist.append(list(grid_dist_line))

        # Find start position while we're iterating over the data
        if S_found:
            continue

        for i in range(line_len):
            if line[i] == 'S':
                S[1] = i
                S_found = True
                break

        if S_found:
            continue

        S[0] += 1

def calculate_max_distance(grid, S) -> int:
    y, x = S
    move = None
    dist = 1

    # Walk through the pipes until we reach back to S
    while True:
        y, x, move = next_tile(y, x, move)
        grid_dist[y][x] = dist

        if grid[y][x] == 'S':
            break

        dist += 1

    return int(dist / 2)

def next_tile(y: int, x: int, last_move: str) -> tuple[int, int, str]:
    # If we start,
    if grid[y][x] == 'S':
         # up?
        if y > 0 and grid[y - 1][x] in ['|', 'F']:
            delta, move  = [-1, 0], 'up'

        # right?
        if x < line_len and grid[y][x + 1] in ['-', '7']:
            delta, move = [0, 1], 'right'

    else:
        symbol = grid[y][x]
        if symbol in ['-', '|']:
            delta = move_to_steps[last_move]
            move = last_move

        else:
            move = move_map[symbol][last_move]
            delta = move_to_steps[move]

    return [y + delta[0], x + delta[1], move]

if len (sys.argv) != 2:
	print("Usage: 10.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        parse_file(file_fh)
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {calculate_max_distance(grid, S)}")
