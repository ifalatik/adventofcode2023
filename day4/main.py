import re

REGEX = r'.*:(?P<winning>.+?(?=\|))\|(?P<picks>.*)$'


def get_nums(s: str) -> list[int]:
    # in: "83 86  6 31 17  9 48 53"
    #
    # out: [83, 86, 6, 31, 17, 9, 48, 53]
    res = []
    num_str = ""
    for c in s:
        if re.search(r'\d', c):
            num_str += c
        elif num_str:
            res.append(int(num_str))
            num_str = ""
    res.append(int(num_str))
    return res

def get_num_wins(winning_numbers: list[int], picks: list[int]) -> int:
    res = 0
    for winning_number in winning_numbers:
        if winning_number in picks:
            res += 1
    return res

def get_points(num_wins: int) -> int:
    if not num_wins:
        return 0
    else:
        return 2**(num_wins-1)


def one(in_lines: list[str]) -> int:
    points = 0
    for card in in_lines:
        if not card:
            continue
        re_match = re.match(REGEX, card)
        if not re_match:
            print(f"No match found! - {card}")
        winning_numbers = get_nums(re_match.group('winning').strip())
        picks = get_nums(re_match.group('picks').strip())
        cur_points = get_points(get_num_wins(winning_numbers, picks))
        points += cur_points
        print(f"Card {card} got {cur_points} points.")
    return points


def two(in_lines: list[str]) -> int:
    total_processed_cards = 0
    card_process_amount = [1 for _ in range(len(in_lines))]
    # process card i card_process_amount[i] times
    for i, card in enumerate(in_lines):
        if not card:
            continue
        # get number of wins for card
        re_match = re.match(REGEX, card)
        if not re_match:
            print(f"No match found! - {card}")
        winning_numbers = get_nums(re_match.group('winning').strip())
        picks = get_nums(re_match.group('picks').strip())
        wins_for_card = get_num_wins(winning_numbers, picks)

        # pretend to have processed the card card_process_amount[i] of times
        total_processed_cards += card_process_amount[i]
        # print(f"Processed card {i+1} - {card_process_amount[i]} time(s)")
        # "copy" the next wins_for_card cards as many times, as card would've been processed
        for j in range(wins_for_card):
            card_process_amount[i+j+1] += card_process_amount[i]
    return total_processed_cards

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    res = two(lines)
    print(f"Total: {res}")
