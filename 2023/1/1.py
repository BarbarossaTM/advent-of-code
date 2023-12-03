#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Sat 02 Dec 2023 02:44:41 PM CET
#

import re
import sys

re_num_strings = re.compile(r'([0-9]|zero|one|two|three|four|five|six|seven|eight|nine)')

string_map = {
	'0'     : 0,
	'1'     : 1,
	'2'     : 2,
	'3'     : 3,
	'4'     : 4,
	'5'     : 5,
	'6'     : 6,
	'7'     : 7,
	'8'     : 8,
	'9'     : 9,
	'zero'  : 0,
	'one'   : 1,
	'two'   : 2,
	'three' : 3,
	'four'  : 4,
	'five'  : 5,
	'six'   : 6,
	'seven' : 7,
	'eight' : 8,
	'nine'  : 9,
}

def get_line_value(line: str) -> int:
	nums = []

	# Finding the first number is rather straight forward, just start searching from the left
	matches = re_num_strings.findall(line)
	if not matches:
		raise Exception(f"Didn't finy any number in '{line}', dying of shame!")

	nums.append(string_map[matches[0]])

	# Finding the last num string is more tricky as re.find* only matches non-overlapping
	# strings, but they may overlap in reality, bummer. So we start searching from the end
	# of the string.
	line_len = len(line)
	for n in range(1, line_len + 1):
		word = line[-n:]

		matches = re_num_strings.findall(word)
		if matches:
			nums.append(string_map[matches[0]])
			break

	if len(nums) < 1:
		raise Exception(f"No numbers found in line: {line}")

	#print (f"{line} -> {nums} ]=> {nums[0] * 10 + nums[-1]}")
	return nums[0] * 10 + nums[-1]

if len (sys.argv) != 2:
	print("Usage: 1.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]
sum = 0

try:
	with open (file_path, "r") as file_fh:
		for line in file_fh.readlines():
			sum += get_line_value(line.strip())
except IOError as e:
	print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
	sys.exit(1)

print(f"Sum: {sum}")

#for word in ['xxonetwonexx', 'xxoneightonexx', 'ninetwonine', 'a1twoa', 'oneight']:
#	print (get_line_value(word))