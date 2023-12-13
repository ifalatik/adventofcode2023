from typing import Optional


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
                if tiles[max(0, 2*split_index - width):split_index][::-1] != tiles[split_index:split_index*2]:
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


def one(input_lines: list[str]) -> int:
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
    result = 0
    for field in fields:
        result += field.get_points()
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        in_lines = f.readlines()
    print(one(in_lines))
