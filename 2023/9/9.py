#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 11 Dec 2023 10:56:23 PM CET
#

import sys
from typing import Optional


sequences = [
    # <int>, ...
]

def parse_line(line: str) -> None:
    sequences.append([int(x) for x in line.split()])

def OASIS(sequences: list[list[int]]) -> int:
    sum = 0

    for seq in sequences:
        sum += extrapolate_next_value(seq)

    return sum

def extrapolate_next_value(values: list[int]) -> int:
    if all_zeros(values):
        return 0

    diffs = compute_differences(values)

    return values[-1] + extrapolate_next_value(diffs)


def compute_differences(values: list[int]) -> list[int]:
    diffs = []
    num_values = len(values)

    for i in range(num_values):
        if i == num_values - 1:
            break

        diffs.append(values[i + 1] - values[i])

    return diffs

def all_zeros(values: list[int]) -> bool:
    for v in values:
        if v != 0:
            return False

    return True

if len (sys.argv) != 2:
	print("Usage: 9.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        for line in file_fh:
            parse_line(line.strip())
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {OASIS(sequences)}")
