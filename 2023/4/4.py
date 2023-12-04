#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 04 Dec 2023 10:01:13 AM CET
#

import json
import sys

data_map = [
    # {
    #   card_id : <int>,
    #   copies  : <int>,
    #   winning : [],
    #   actual  : [],
    # }
]
points = 0

def calculate_points_for_card(winning: list[int], actual: list[int]) -> (int, int):
    points = 0
    matches = 0

    for number in actual:
        if number not in winning:
            continue

        matches += 1
        if points == 0:
            points = 1
        else:
            points *= 2

    return points, matches

def mark_copies(card_id: int, next_cards: int) -> None:
    copies = data_map[card_id-1]['copies'] + 1

    for id in range (card_id, card_id + next_cards):
        data_map[id]['copies'] += copies

def calculate_points(data_map: list) -> int:
    points = 0

    for card in data_map:
        card_points, matches = calculate_points_for_card(card['winning'], card['actual'])
        points += card_points
        card['matches'] = matches
        mark_copies(card['id'], matches)

    return points

def calculate_cards(data_map: list) -> int:
    cards = 0

    for card in data_map:
        cards += card['copies'] + 1

    return cards

def parse_line(line: str) -> None:
    card_str, numbers = line.split(':', 2)
    winning_str, actual_str = numbers.split('|')

    card_id = int(card_str.split()[1])
    winning = winning_str.split()
    actual = actual_str.split()

    data_map.append(
        {
            "id" : card_id,
            "copies" : 0,
            "winning": winning,
            "actual": actual,
        }
    )

if len (sys.argv) != 2:
	print("Usage: 4.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        for line in file_fh.readlines():
            parse_line(line.strip())
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {calculate_points(data_map)}")
print(f"Part 2: {calculate_cards(data_map)}")
