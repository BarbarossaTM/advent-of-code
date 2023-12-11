#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 11 Dec 2023 09:18:20 PM CET
#

import re
import sys

re_line = re.compile(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)')

# LLR
#
# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)

pattern = []
data_map = {
    # [ <str>, <str> ],
}

def parse_line(line: str) -> None:
    if line == "":
        return
    
    match = re_line.search(line)
    if not match:
        raise Exception(f"Line didn't match: {line}")
    
    data_map[match.group(1)] = [
        match.group(2),
        match.group(3),
    ]

def trace_path(data_map) -> int:
    """
    Trace the path from AAA to ZZZ and count the steps.
    """
    steps = 0
    i = 0

    node = 'AAA'

    while node != 'ZZZ':
        #old_node = node
        index = 0 if pattern[i] == 'L' else 1
        node = data_map[node][index]
        #print(f"Node {old_node} + {pattern[i]} -> {node}")

        i = (i + 1) % len(pattern)    # Treat pattern list as ring buffer
        steps +=1

    return steps

if len (sys.argv) != 2:
	print("Usage: 8.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        pattern = list(file_fh.readline().strip())

        for line in file_fh:
            parse_line(line.strip())
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {trace_path(data_map)}")