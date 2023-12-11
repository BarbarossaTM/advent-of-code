#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 11 Dec 2023 09:18:20 PM CET
#

from math import lcm
import re
import sys

re_line = re.compile(r'(\w+) = \((\w+), (\w+)\)')

# LLR
#
# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)

pattern = []
starters = []
data_map = {
    # <str>: [ <str>, <str> ],
}

def parse_line(line: str) -> None:
    if line == "":
        return
    
    match = re_line.search(line)
    if not match:
        raise Exception(f"Line didn't match: {line}")
    
    start, left, right = match.group(1), match.group(2), match.group(3)

    data_map[start] = [ left, right ]

    if start.endswith('A'):
        starters.append(start)

def trace_path_part1(data_map) -> int:
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

def trace_path_part2(data_map) -> int:
    """
    Trace the path from AAA to ZZZ and count the steps.
    """
    paths = [
        # {
        #   'node' : <str>,
        # }
    ]

    # Set up paths
    for start in starters:
        paths.append({
            'node': start,
            'steps': 0,
        })

    for path in paths:
        steps = 0
        i = 0

        while not path['node'].endswith('Z'):
            index = 0 if pattern[i] == 'L' else 1
            path['node'] = data_map[path['node']][index]

            i = (i + 1) % len(pattern)    # Treat pattern list as ring buffer
            steps +=1

        path['steps'] = steps

    return lcm(*[path['steps'] for path in paths])

def all_paths_resolved(paths: list[dict]) -> bool:
    for path in paths:
        if not path['node'].endswith('Z'):
            return False

    return True

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

print(f"Part 1: {trace_path_part1(data_map)}")
print(f"Part 2: {trace_path_part2(data_map)}")