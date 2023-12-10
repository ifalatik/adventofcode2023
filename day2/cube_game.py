import re
from builtins import getattr
from enum import Enum


class Color(Enum):
    red = 1
    green = 2
    blue = 3


class GameRound:
    id: int
    sets: list[dict[Color, int]]

    @staticmethod
    def _get_game_id(record: str) -> int:
        id_regex = r'^Game\ (\d+):'
        return int(re.search(id_regex, record).groups()[0])

    @staticmethod
    def _parse_color_and_amount(num_and_color: str) -> tuple[Color, int]:
        num_and_color = num_and_color.strip()
        num_str, color_str = num_and_color.split(' ')
        return getattr(Color, color_str), int(num_str)

    @staticmethod
    def _get_sets(record: str) -> list[dict[Color, int]]:
        # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        result = []
        # remove everything in front of the colon
        sub_record = record[record.index(':') + 1:]
        # split into sets
        set_strings = sub_record.split(';')
        for idx, set_str in enumerate(set_strings):
            d = {}
            # split into list of number and color
            num_and_color_strings = set_str.split(',')
            for num_and_color_string in num_and_color_strings:
                color, amount = GameRound._parse_color_and_amount(num_and_color_string)
                d[color] = amount
            result.append(d)
        return result

    def __init__(self, record: str):
        self.id = GameRound._get_game_id(record)
        self.sets = GameRound._get_sets(record)

    def get_max_for_color(self, color: Color) -> int:
        _max = 0
        for _set in self.sets:
            if (_set.get(color) or 0) > _max:
                _max = _set[color]
        return _max


def one(in_lines: list[str]) -> int:
    max_amounts = {Color.red: 12, Color.green: 13, Color.blue: 14}
    sum_possible_round_ids = 0
    for line in in_lines:
        gr = GameRound(line)
        for color in max_amounts.keys():
            if gr.get_max_for_color(color) > max_amounts[color]:
                break
        else:
            sum_possible_round_ids += gr.id
    return sum_possible_round_ids


def two(in_lines: list[str]) -> int:
    sum_powers_colors = 0
    for line in in_lines:
        gr = GameRound(line)
        max_amounts_for_colors = [gr.get_max_for_color(color) for color in Color]
        if not any(max_amounts_for_colors):  # if all are 0 ignore round
            continue
        power = 1
        for amount in max_amounts_for_colors:
            power *= amount or 1
        sum_powers_colors += power
    return sum_powers_colors


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_lines = f.readlines()
    print(one(input_lines))
    print(two(input_lines))
