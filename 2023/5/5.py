#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sun 10 Dec 2023 11:00:11 PM CET
#

import json
import sys

data_map = {
    'seeds' : [],   # [<int>]
    # "<x>-to-<y>": [],
    # }
}

def parse_file(fh) -> None:
    active_map = None

    for line in file_fh.readlines():
        line = line.strip()

        # Empty line between maps
        if line == "":
             continue

        # Seeds
        if line.startswith("seeds:"):
            elements = line.split()
            for seed_str in elements[1:]:
                data_map['seeds'].append(int(seed_str))

            continue

        # Start of new map
        if line.endswith('map:'):
            map_key = line.split()[0]

            active_map = []
            data_map[map_key] = active_map

            continue

        # Regular map line
        # Format: dst range start, src range start, range length
        fields = line.split()

        active_map.append({
            'dst_range_start' : int(fields[0]),
            'src_range_start' : int(fields[1]),
            'range_len'       : int(fields[2]),
        })


def map_value(map_key: str, value: int) -> int:
    entries = data_map[map_key]

    for entry in entries:
        if value >= entry['src_range_start'] and value <= entry['src_range_start'] + entry['range_len']:
            offset = entry['src_range_start'] - entry['dst_range_start']
            return value - offset
        
    return value

def map_seed_to_location(value: int) -> int:
    ret = value

    for transition in [
        'seed-to-soil',
        'soil-to-fertilizer',
        'fertilizer-to-water',
        'water-to-light',
        'light-to-temperature',
        'temperature-to-humidity',
        'humidity-to-location',
    ]:
        ret = map_value(transition, ret)

    return ret

def calculate_lowest_location(data_map: dict) -> int:
    min_location = None

    for seed in data_map['seeds']:
        loc = map_seed_to_location(seed)
        if min_location is None:
            min_location = loc
            continue

        if loc < min_location:
            min_location = loc

    return min_location


if len (sys.argv) != 2:
	print("Usage: 5.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        parse_file(file_fh)
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {calculate_lowest_location(data_map)}")

#print(json.dumps(data_map, indent=4))

## Verification
#for src, dst in {
#    13: 13,
#    14: 14,
#    55: 57,
#    79: 81,
#    98: 50,
#}.items():
#    mapped_value = map_value('seed-to-soil', src)
#    if mapped_value == dst:
#        print(".", end="")
#    else:
#        print("!", end="")
#
#print("")
