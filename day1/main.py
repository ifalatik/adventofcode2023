import re


def get_calibration_value(in_line: str) -> int:
    val = ''
    for char in in_line:
        if re.fullmatch(r'\d', char):
            val += char
            break
    else:  # if we never break, no digit is detected and we can return 0
        return 0
    for char in reversed(in_line):
        if re.fullmatch(r'\d', char):
            val += char
            break
    return int(val)


def one(in_lines: list[str]) -> int:
    return sum(get_calibration_value(line) for line in in_lines)


def to_int(in_str: str) -> int:
    if len(in_str) == 1:
        return int(in_str)
    return {'one': 1, 'two': 2, 'three': 3, 'four': 4,
            'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
            'nine': 9}[in_str]


def get_calibration_value_with_text(in_line: str) -> int:
    regex = r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))'
    matches = re.findall(regex, in_line)
    if not matches:
        return 0
    val = to_int(matches[0])*10
    val += to_int(matches[-1])
    return val


def two(in_lines: list[str]) -> int:
    return sum(get_calibration_value_with_text(line) for line in in_lines)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_lines = f.readlines()
    print(one(input_lines))
    print(two(input_lines))
