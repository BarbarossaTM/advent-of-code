#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sun 17 Dec 2023 09:14:23 PM CET
#

import sys

values = []

def hash(text) -> int:
    hash_val = 0

    for char in text:
        hash_val = ((hash_val + ord(char)) * 17) % 256

    return hash_val

def hash_values(values: list[str]) -> int:
    val = 0

    for text in values:
        val += hash(text)

    return val

if len (sys.argv) != 2:
	print("Usage: 15.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        text = file_fh.readline().strip()

        values = text.split(',')
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {hash_values(values)}")