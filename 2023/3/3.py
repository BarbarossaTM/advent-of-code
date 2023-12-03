#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sun 03 Dec 2023 09:53:51 PM CET
#

import sys

data_map = []

def is_symbol(char: str) -> bool:
    return not char.isdigit() and char != '.'

def is_eligible(line_no: int , index: int) -> bool:
#    print(f"Checking {line_no}/{index}")
    # If we're checking line 2 or above, look into the line above
    if line_no > 0:
#        print(f"is_eligible(): line 1+")
        prev_line = data_map[line_no - 1]
        for i in [ index - 1, index, index + 1]:
            # Make sure we're staying inside the bounds of the array
            if i < 0 or i > len(prev_line) - 1:
                continue

            if is_symbol(prev_line[i]):
                return True

    # Check left of "us"
    line = data_map[line_no]
    if index - 1 > 0 and is_symbol(line[index - 1]):
#        print(f"is_eligible(): left-of-us")
        return True
    
    if index + 1 < len(line) and is_symbol(line[index + 1]):
#        print(f"is_eligible(): right-of-us")
        return True
    
    # Check next line, if we aren't on the last one already
    if line_no < len(data_map) - 1:
        next_line = data_map[line_no + 1]
#        print(f"is_eligible(): non-last-line")
        for i in [ index - 1, index, index + 1]:
            # Make sure we're staying inside the bounds of the array
            if i < 0 or i > len(next_line) - 1:
                continue

            if is_symbol(next_line[i]):
#                print(f"is_eligible(): {line_no + 1}/{i}: {data_map[line_no + 1][i]}")
                return True
    
    return False

def get_part_no(data_map: list) -> int:
    part_no = 0
    line_no = 0

    for line in data_map:
        char_no = 0
        number = ""
        eligible = False

        for char in line:
            #print(f"Reading '{char}'")
            if char.isdigit():
                number += char
                if not eligible and is_eligible(line_no, char_no):
#                    print(f"{line_no}/{char_no} is eligible")
                    eligible = True

            else:
                if eligible:
                    print(f"{number}", end=" ")
                    part_no += int(number)
                    eligible = False

                number = ""

            char_no += 1

        if eligible:
            print(f"{number}", end=" ")
            part_no += int(number)

        print("")
        line_no += 1

    return part_no

if len (sys.argv) != 2:
	print("Usage: 3.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        line_no = 0
        for line in file_fh.readlines():
            data_map.append(list(line.strip()))

        line_no += 1
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print (f"Part 1: {get_part_no(data_map)}")