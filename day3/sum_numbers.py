import re
from dataclasses import dataclass

SYMBOL_REGEX = r'[^\d.]'
NUMBER_REGEX = r'\d+'


@dataclass
class Number:
    x: int
    y: int
    value: int


class Engine:
    schematic: list[list[str]]

    def __init__(self, in_lines: list[str]):
        self.schematic = []
        for line in in_lines:
            if not line:
                continue
            self.schematic.append([character for character in line.strip()])

    def _get_surrounding_numbers(self, x, y) -> list[Number]:
        result = []
        # get all numbers above
        if y != 0:
            for number_match in re.finditer(NUMBER_REGEX, ''.join(self.schematic[y - 1])):
                if x in range(number_match.start(0) - 1, number_match.end(0) + 1):
                    result.append(Number(number_match.start(0), y - 1, int(number_match.group(0))))
        # get all numbers below
        if y != len(self.schematic) - 1:
            for number_match in re.finditer(NUMBER_REGEX, ''.join(self.schematic[y + 1])):
                if x in range(number_match.start(0) - 1, number_match.end(0) + 1):
                    result.append(Number(number_match.start(0), y + 1, int(number_match.group(0))))
        # get number to the left
        if x != 0:
            number_match = re.search(NUMBER_REGEX + '$', ''.join(self.schematic[y][:x]))
            if number_match:
                result.append(Number(number_match.start(0), y, int(number_match.group(0))))
        # get number to the right
        if x != len(self.schematic[0]) - 1:
            number_match = re.search('^' + NUMBER_REGEX, ''.join(self.schematic[y][x + 1:]))
            if number_match:
                result.append(Number(x + 1, y, int(number_match.group(0))))
        return result

    def get_relevant_numbers(self) -> list[int]:
        result = []
        for y, char_list in enumerate(self.schematic):
            for symbol_match in re.finditer(SYMBOL_REGEX, ''.join(char_list)):
                surrounding_numbers = self._get_surrounding_numbers(symbol_match.start(0), y)
                for surrounding_number in surrounding_numbers:
                    if surrounding_number not in result:
                        result.append(surrounding_number)
        return [n.value for n in result]

    def get_gear_ratios(self) -> list[int]:
        number_pairs = []
        for y, char_list in enumerate(self.schematic):
            for symbol_match in re.finditer(r'\*', ''.join(char_list)):
                surrounding_numbers = self._get_surrounding_numbers(symbol_match.start(0), y)
                if len(surrounding_numbers) == 2:
                    if surrounding_numbers not in number_pairs:
                        number_pairs.append(surrounding_numbers)
        return [n1.value * n2.value for n1, n2 in number_pairs]


def one(in_lines: list[str]) -> int:
    engine = Engine(in_lines)
    return sum(engine.get_relevant_numbers())


def two(in_lines: list[str]) -> int:
    engine = Engine(in_lines)
    return sum(engine.get_gear_ratios())


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_lines = f.readlines()
    print(one(input_lines))
    print(two(input_lines))
