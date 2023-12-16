from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Tile:
    x: int
    y: int
    _character: str
    _visited_in_directions: list[Direction]

    def __init__(self, char: str, x: int, y: int):
        if len(char) != 1:
            raise Exception(f"Character {char} can't be converted to Tile as length is not one.")
        self._character = char
        self.x = x
        self.y = y
        self._visited_in_directions = []

    def __str__(self):
        return f"({self.x}, {self.y}): {self._character} | {self._visited_in_directions}"

    def _get_next_directions(self, in_direction: Direction) -> list[Direction]:
        match self._character:
            case '.':
                return [in_direction]
            case '|':
                if in_direction == Direction.NORTH or in_direction == Direction.SOUTH:
                    return [in_direction]
                return [Direction.NORTH, Direction.SOUTH]
            case '-':
                if in_direction == Direction.EAST or in_direction == Direction.WEST:
                    return [in_direction]
                return [Direction.EAST, Direction.WEST]
            case '\\':  # 0 -> 3, 1 -> 2, 2 -> 1, 3 -> 0
                return [[Direction.WEST, Direction.SOUTH, Direction.EAST, Direction.NORTH][in_direction.value]]
            case '/':  # 0 -> 1, 1 -> 0, 2 -> 3, 3 -> 2
                return [[Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH][in_direction.value]]

    def visit_from_direction(self, in_direction: Direction) -> list[Direction]:
        if in_direction in self._visited_in_directions:
            return []
        self._visited_in_directions.append(in_direction)
        return self._get_next_directions(in_direction)

    @property
    def visited(self) -> bool:
        return bool(self._visited_in_directions)

    def reset_visits(self) -> None:
        self._visited_in_directions = []

@dataclass
class Step:
    tile: Tile
    in_direction: Direction


class LaserBeamsGame:
    game_field: list[list[Tile]]

    def __init__(self, in_lines: list[str]):
        self.game_field = []
        for y, line in enumerate(in_lines):
            if not line:
                continue
            self.game_field.append([Tile(character, x, y) for x, character in enumerate(line.strip())])

    def _get_next_steps(self, cur_step: Step) -> list[Step]:
        result = []
        for out_direction in cur_step.tile.visit_from_direction(cur_step.in_direction):
            match out_direction:
                case Direction.NORTH:
                    if cur_step.tile.y == 0:
                        continue
                    result.append(Step(self.game_field[cur_step.tile.y - 1][cur_step.tile.x], out_direction))
                case Direction.EAST:
                    if cur_step.tile.x == len(self.game_field[0]) - 1:
                        continue
                    result.append(Step(self.game_field[cur_step.tile.y][cur_step.tile.x + 1], out_direction))
                case Direction.SOUTH:
                    if cur_step.tile.y == len(self.game_field) - 1:
                        continue
                    result.append(Step(self.game_field[cur_step.tile.y + 1][cur_step.tile.x], out_direction))
                case Direction.WEST:
                    if cur_step.tile.x == 0:
                        continue
                    result.append(Step(self.game_field[cur_step.tile.y][cur_step.tile.x - 1], out_direction))
        return result

    def reset_visits(self):
        for row in self.game_field:
            for tile in row:
                tile.reset_visits()

    def shoot_laser(self, start_step: Step):
        if not self.game_field:
            return
        self.reset_visits()
        cur_steps = [start_step]
        while cur_steps:
            next_steps = []
            for step in cur_steps:
                next_steps += self._get_next_steps(step)
            cur_steps = next_steps

    def get_visited_fields(self) -> int:
        visited_fields = 0
        for row in self.game_field:
            for tile in row:
                visited_fields += int(tile.visited)
        return visited_fields


def one(in_lines: list[str]) -> int:
    laser_beams_game = LaserBeamsGame(in_lines)
    laser_beams_game.shoot_laser(Step(laser_beams_game.game_field[0][0], Direction.EAST))
    return laser_beams_game.get_visited_fields()


def two(in_lines: list[str]) -> int:
    laser_beams_game = LaserBeamsGame(in_lines)
    max_visited_fields = 0
    # from top
    for tile in laser_beams_game.game_field[0]:
        laser_beams_game.shoot_laser(Step(tile, Direction.SOUTH))
        max_visited_fields = max(max_visited_fields, laser_beams_game.get_visited_fields())
    # from bottom
    for tile in laser_beams_game.game_field[-1]:
        laser_beams_game.shoot_laser(Step(tile, Direction.NORTH))
        max_visited_fields = max(max_visited_fields, laser_beams_game.get_visited_fields())
    for row in laser_beams_game.game_field:
        # from left
        laser_beams_game.shoot_laser(Step(row[0], Direction.EAST))
        max_visited_fields = max(max_visited_fields, laser_beams_game.get_visited_fields())
        # from right
        laser_beams_game.shoot_laser(Step(row[-1], Direction.WEST))
        max_visited_fields = max(max_visited_fields, laser_beams_game.get_visited_fields())
    return max_visited_fields


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_lines = f.readlines()
    print(one(input_lines))
    print(two(input_lines))
