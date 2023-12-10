#!/usr/bin/python3
#
# Maximilian Wilhelm <max@sdn.clinic>
#  --  Mon 11 Dec 2023 12:13:14 AM CET
#

from functools import cmp_to_key
import sys

entries = [
    # {
    #    'cards' : [ <str> ],
    #    'bid'   : <int>,
    #    'type:  : <int>,
    # } 
]

card_strength_map = {
    'A' : 13,
    'K' : 12,
    'Q' : 11,
    'J' : 10,
    'T' :  9,
    '9' :  8,
    '8' :  7,
    '7' :  6,
    '6' :  5,
    '5' :  4,
    '4' :  3,
    '3' :  2,
    '2' :  1,
}

hand_types = {
    'five_of_a_kind' : 7,   # All cards are the same
    'four_of_a_kind' : 6,   # Four cards are the same
    'full_house'     : 5,   # Two cards X and three card Y
    'three_of_a_kind': 4,   # Three cards are the same, two are distinct
    'two_pair'       : 3,   # Two cards X, two cards Y, one card Z
    'one_pair'       : 2,   # Two cards X, three distinct !X cards
    'high_card'      : 1,   # Five distinct cards
}


def parse_line(line: str) -> None:
    cards_str, bid_str = line.split()

    cards = list(cards_str)

    entries.append({
        'cards': cards,
        'bid'  : int(bid_str),
        'type' : classify_hand_type(cards),
    })

def classify_hand_type(cards: list[str]) -> int:
    card_count = {}
    max_count = 0

    for card in cards:
        if card not in card_count:
            card_count[card] = 0

        card_count[card] += 1

        if card_count[card] > max_count:
            max_count += 1

    if max_count == 5:
        return hand_types['five_of_a_kind']

    if max_count == 4:
        return hand_types['four_of_a_kind']

    if max_count == 3:
        for count in card_count.values():
            if count == 2:
                return hand_types['full_house']
            
            if count == 1:
                return hand_types['three_of_a_kind']
            
    if max_count == 2:
        twos = []
        ones = []
        for card, count in card_count.items():
            if count == 2:
                twos.append(card)
            if count == 1:
                ones.append(card)

        if len(twos) == 2:
            return hand_types['two_pair']
    
        if len(twos) == 1 and len(ones) == 3:
            return hand_types['one_pair']
        
    if max_count == 1:
        return hand_types['high_card']

def cmp_hands(entry_a: dict, entry_b: dict) -> int:
    """
    Return -1 is if a < b, 0 if a == b, and 1 if a > b.
    """

    # If the hand types are different, they decice the fate
    if entry_a['type'] != entry_b['type']:
        return entry_a['type'] - entry_b['type']
    
    # If they are equal we need to compare cards
    cards_a = entry_a['cards']
    cards_b = entry_b['cards']
    for i in range(0, 5):
        card_a = cards_a[i]
        card_b = cards_b[i]
        if card_a == card_b:
            continue

        return card_strength_map[card_a] - card_strength_map[card_b]

def compute_winnings(entries) -> int:
    winnings = 0

    # Sort entries to get the ranks
    sorted_entries = sorted(entries, key=cmp_to_key(cmp_hands))

    for i in range(len(entries)):
        rank = i + 1
        winnings += rank * sorted_entries[i]['bid']

    return winnings

if len (sys.argv) != 2:
	print("Usage: 7.py file_path", file=sys.stderr)
	sys.exit(1)

file_path = sys.argv[1]

try:
    with open (file_path, "r") as file_fh:
        for line in file_fh.readlines():    
            parse_line(line.strip())
except IOError as e:
    print(f"File to open '{file_path}': {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"Part 1: {compute_winnings(entries)}")