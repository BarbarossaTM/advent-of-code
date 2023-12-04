#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 04 Dec 2023 10:01:13 AM CET
#

import sys

data_map = [
    # {
    #   winning : [],
    #   actual : [],
    # }
]
points = 0

def calculate_points(winning: list[int], actual: list[int]) -> int:
    points = 0

    for number in actual:
        if number not in winning:
            continue

        if points == 0:
            points = 1
        else:
            points *= 2

    return points

def parse_line(line: str) -> int:
    card, numbers = line.split(':', 2)
    winning_str, actual_str = numbers.split('|')

    winning = winning_str.split()
    actual = actual_str.split()

    data_map.append(
        {
            "winning": winning,
            "actual": actual,
        }
    )

    return calculate_points(winning, actual)


if len (sys.argv) != 2:
	print("Usage: 4.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        for line in file_fh.readlines():
            points += parse_line(line.strip())
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {points}")
