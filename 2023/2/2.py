#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sun 03 Dec 2023 09:01:00 PM CET
#

import re
import sys

re_game = re.compile(r'Game (\d+):')
re_result = re.compile(r'(\d+) (\w+)')

max_color_values_by_game = {
	# 1 : {
    #   'green' : 1,
    #   ...
    # }
}

def set_game_stats_max(game_id: str, values: dict) -> None:
    if game_id not in max_color_values_by_game:
        max_color_values_by_game[game_id] = {}

    curvals = max_color_values_by_game[game_id]

    for k, v in values.items():
        if k not in curvals or int(v) > int(curvals[k]):
            curvals[k] = v


def handle_line(line: str) -> None:
    match = re_game.search(line)
    if not match:
        raise Exception(f"Failed to find game in line {line}")

    game_id = match.group(1)
	
    results_string = line.split(':')[1]
    results = results_string.split(';')

    for result in results:
        stats = {}

        matches = re.findall(r'(\d+) (\w+)', result)
        if not matches:
            raise Exception(f"Failed to parse results: {result}")

        for match in matches:
            stats[match[1]] = match[0]

        set_game_stats_max(game_id, stats)

if len (sys.argv) != 2:
	print("Usage: 2.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
	with open (file_path, "r") as file_fh:
		for line in file_fh.readlines():
			handle_line(line.strip())
except IOError as e:
	print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
	sys.exit(1)

# Part 1:
# The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

min_values = {
    'red' : 12,
    'green' : 13,
    'blue' : 14,
}

game_id_sum = 0
for game_id in sorted(max_color_values_by_game.keys()):
    stats = max_color_values_by_game[game_id]

    ignore_name = False
    for k,v in min_values.items():
        if int(stats.get(k, 0)) > v:
            ignore_name = True

    if ignore_name:
         continue

    game_id_sum += int(game_id)

print (game_id_sum)