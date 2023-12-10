#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sun 10 Dec 2023 11:48:12 PM CET
#

import sys

matches = [
    # {
    #    'time' : <int>,
    #    'distance' : <int>,
    #    'winning_times : [ <int> ],
    # } 
]

def parse_file(fh) -> None:
    for line in file_fh.readlines():
        line = line.strip()

        if line.startswith('Time:'):
            for time in line.split(':')[1].split():
                matches.append({
                    'time': int(time),
                    'winning_games': [],
                })

        if line.startswith('Distance:'):
            distances = line.split(':')[1].split()
            for i in range(len(distances)):
                matches[i]['distance'] = int(distances[i])

def calculate_winning_games(data_map: dict) -> int:
    wins = 1

    for game in matches:
        possible_win = 0

        game_duration = game['time']

        for charge_time in range(game_duration):
            drive_time = game_duration - charge_time
            game_distance = charge_time * drive_time

            # If we moved further than the previous record, we win!
            if game_distance > game['distance']:
                game['winning_games'].append(charge_time)
                possible_win += 1

        wins *= possible_win

    return wins

def calculate_winning_game(data_map: dict) -> int:
    possible_wins = 0

    time_str = ""
    distance_str = ""

    for game in matches:
        time_str += str(game['time'])
        distance_str += str(game['distance'])

    game_duration = int(time_str)
    distance = int(distance_str)

    for charge_time in range(game_duration):
        drive_time = game_duration - charge_time
        game_distance = charge_time * drive_time

        # If we moved further than the previous record, we win!
        if game_distance > distance:
            game['winning_games'].append(charge_time)
            possible_wins += 1

    return possible_wins


if len (sys.argv) != 2:
	print("Usage: 6.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        parse_file(file_fh)
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {calculate_winning_games(matches)}")
print(f"Part 2: {calculate_winning_game(matches)}")
