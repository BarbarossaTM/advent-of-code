#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sat 02 Dec 2023 02:44:41 PM CET
#

import re
import sys

def handle_line(line):
	global sum

	nums = []

	for char in line:
		if char < '0' or char > '9':
			continue

		nums.append(char)

	if len(nums) < 1:
		raise Exception(f"No numbers found in line: {line}")

	sum += int (f"{nums[0]}{nums[-1]}")

if len (sys.argv) != 2:
	print("Usage: 1.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]
sum = 0

try:
	with open (file_path, "r") as file_fh:
		for line in file_fh.readlines():
			handle_line(line)
except IOError as e:
	print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
	sys.exit(1)

print(f"Sum: {sum}")
