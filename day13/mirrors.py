from typing import Optional, Iterable


class Field:
    _tiles_list: list[str]

    def __init__(self):
        self._tiles_list = []

    def __str__(self) -> str:
        res = ""
        for tile in self._tiles_list:
            res += tile + '\n'
        return res

    def append_to_tiles(self, line_of_tiles: str) -> None:
        self._tiles_list.append(line_of_tiles.strip())

    def _get_points_vertical(self) -> Optional[int]:
        """
        :return: # of columns left to a vertical mirror if it exists
        """
        # iterate from 1 to len(width)-1 as we can never split on the first or last index
        width = len(self._tiles_list[0])
        for split_index in range(1, width):
            for tiles in self._tiles_list:
                if tiles[max(0, 2 * split_index - width):split_index][::-1] != tiles[split_index:split_index * 2]:
                    break
            else:  # never hit a break
                return split_index
        return None

    def _get_points_horizontal(self) -> Optional[int]:
        """
        :return: # of rows times 100, above a horizontal mirror if it exists
        """
        # iterate from 1 to len(height)-1 as we can never split on the first or last index
        for split_index in range(1, len(self._tiles_list)):
            for tiles_before_split, tiles_after_split in zip(  # zip only returns tuples for the minimum length
                    reversed(self._tiles_list[:split_index]),
                    self._tiles_list[split_index:]):
                if tiles_before_split != tiles_after_split:
                    break
            else:  # never hit a break
                return split_index * 100
        return None

    def get_points(self) -> int:
        vertical_points = self._get_points_vertical()
        if vertical_points:
            return vertical_points
        horizontal_points = self._get_points_horizontal()
        if horizontal_points:
            return horizontal_points
        print("Error: no points for:")
        print(self)
        return 0

    @staticmethod
    def _calculate_diff(s1: Iterable, s2: Iterable):
        diff = 0
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                diff += 1
        return diff

    def _get_points_with_smudge_vertical(self) -> Optional[int]:
        width = len(self._tiles_list[0])
        for split_index in range(1, width):
            total_diff_between_tiles = 0
            for tiles in self._tiles_list:
                total_diff_between_tiles += Field._calculate_diff(
                    tiles[max(0, 2 * split_index - width):split_index][::-1],
                    tiles[split_index:split_index * 2]
                )
                if total_diff_between_tiles > 1:
                    break
            if total_diff_between_tiles == 1:  # never hit a break
                return split_index
        return None

    def _get_points_with_smudge_horizontal(self) -> Optional[int]:
        for split_index in range(1, len(self._tiles_list)):
            total_diff_between_tiles = 0
            for tiles_before_split, tiles_after_split in zip(  # zip only returns tuples for the minimum length
                    reversed(self._tiles_list[:split_index]),
                    self._tiles_list[split_index:]):
                total_diff_between_tiles += Field._calculate_diff(tiles_before_split, tiles_after_split)
                if total_diff_between_tiles > 1:
                    break
            if total_diff_between_tiles == 1:  # never hit a break
                return split_index*100
        return None

    def get_points_with_smudge(self) -> int:
        vertical_points = self._get_points_with_smudge_vertical()
        if vertical_points:
            return vertical_points
        horizontal_points = self._get_points_with_smudge_horizontal()
        if horizontal_points:
            return horizontal_points
        print("Error: no points for:")
        print(self)
        return 0


def collect_fields(input_lines: list[str]) -> list[Field]:
    fields: list[Field] = []
    cur_field = Field()
    for line in input_lines:
        if line == '\n':
            fields.append(cur_field)
            cur_field = Field()
        else:
            cur_field.append_to_tiles(line)
    if cur_field:
        fields.append(cur_field)
    return fields


def one(input_lines: list[str]) -> int:
    fields = collect_fields(input_lines)
    result = 0
    for field in fields:
        result += field.get_points()
    return result


def two(input_lines: list[str]) -> int:
    fields = collect_fields(input_lines)
    result = 0
    for field in fields:
        result += field.get_points_with_smudge()
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        in_lines = f.readlines()
    print(one(in_lines))
    print(two(in_lines))
