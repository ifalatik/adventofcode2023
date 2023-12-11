from enum import Enum
from itertools import product
from typing import Optional


class Pipe:
    connected_directions: tuple[Optional['Pipe.Direction'], Optional['Pipe.Direction']]
    ground: bool

    class Direction(Enum):
        NORTH = 0
        EAST = 1
        SOUTH = 2
        WEST = 3

    def __init__(self, character: str):
        if len(character) != 1:
            raise Exception(f"Can't parse character '{character}' to pipe as length isn't 1.")
        if character == '.':
            self.connected_directions = (None, None)
            self.ground = True
        else:
            match character:
                case '|':
                    self.connected_directions = (Pipe.Direction.NORTH, Pipe.Direction.SOUTH)
                case '-':
                    self.connected_directions = (Pipe.Direction.EAST, Pipe.Direction.WEST)
                case 'L':
                    self.connected_directions = (Pipe.Direction.NORTH, Pipe.Direction.EAST)
                case 'J':
                    self.connected_directions = (Pipe.Direction.NORTH, Pipe.Direction.WEST)
                case '7':
                    self.connected_directions = (Pipe.Direction.SOUTH, Pipe.Direction.WEST)
                case 'F':
                    self.connected_directions = (Pipe.Direction.SOUTH, Pipe.Direction.EAST)
                case 'S':
                    self.connected_directions = (None, None)
                case _:
                    raise Exception(f"Can't parse character '{character}' to pipe. Character not found.")
            self.ground = False

    def __str__(self):
        return f"{self.connected_directions[0]}, {self.connected_directions[1]}"


class PipeGame:
    pipes: list[list[Optional[Pipe]]]  # pipes[x][y] starting at (0,0) at the most north and most west point.
    # pipe can be None during initialization but not afterward.
    starting_coordinates: tuple[int, int]  # (x,y)

    def __init__(self, playing_field_lines: list[str]):
        # initialize self.pipes with None values, so we can address the coordinates
        self.pipes = [[None for _ in range(len(playing_field_lines))]
                      for _ in range(len(playing_field_lines[0].strip()))]

        for y, line in enumerate(playing_field_lines):
            line = line.strip()
            for x, char in enumerate(line):
                if char == 'S':
                    self.starting_coordinates = (x, y)
                p = Pipe(char)
                self.pipes[x][y] = p

    def _get_next_pipe_coordinates_and_direction(self, cur_x: int, cur_y: int, direction: Pipe.Direction) -> \
            Optional[tuple[int, int, Pipe.Direction]]:
        """If walking to the starting position, the direction returned will always be North."""
        match direction:
            case Pipe.Direction.NORTH:
                if cur_y == 0:
                    return None
                if self.starting_coordinates[0] == cur_x and self.starting_coordinates[1] == cur_y - 1:
                    return cur_x, cur_y - 1, Pipe.Direction.NORTH

                next_pipe = self.pipes[cur_x][cur_y - 1]
                if Pipe.Direction.SOUTH == next_pipe.connected_directions[0]:
                    return cur_x, cur_y - 1, next_pipe.connected_directions[1]
                elif Pipe.Direction.SOUTH == next_pipe.connected_directions[1]:
                    return cur_x, cur_y - 1, next_pipe.connected_directions[0]
                return None
            case Pipe.Direction.EAST:
                if cur_x == len(self.pipes) - 1:
                    return None
                if self.starting_coordinates[0] == cur_x + 1 and self.starting_coordinates[1] == cur_y:
                    return cur_x + 1, cur_y, Pipe.Direction.NORTH

                next_pipe = self.pipes[cur_x + 1][cur_y]
                if Pipe.Direction.WEST == next_pipe.connected_directions[0]:
                    return cur_x + 1, cur_y, next_pipe.connected_directions[1]
                elif Pipe.Direction.WEST == next_pipe.connected_directions[1]:
                    return cur_x + 1, cur_y, next_pipe.connected_directions[0]
                return None
            case Pipe.Direction.SOUTH:
                if cur_y == len(self.pipes[0]) - 1:
                    return None
                if self.starting_coordinates[0] == cur_x and self.starting_coordinates[1] == cur_y + 1:
                    return cur_x, cur_y + 1, Pipe.Direction.NORTH

                next_pipe = self.pipes[cur_x][cur_y + 1]
                if Pipe.Direction.NORTH == next_pipe.connected_directions[0]:
                    return cur_x, cur_y + 1, next_pipe.connected_directions[1]
                elif Pipe.Direction.NORTH == next_pipe.connected_directions[1]:
                    return cur_x, cur_y + 1, next_pipe.connected_directions[0]
            case Pipe.Direction.WEST:
                if cur_x == 0:
                    return None
                if self.starting_coordinates[0] == cur_x - 1 and self.starting_coordinates[1] == cur_y:
                    return cur_x - 1, cur_y, Pipe.Direction.NORTH

                next_pipe = self.pipes[cur_x - 1][cur_y]
                if Pipe.Direction.EAST == next_pipe.connected_directions[0]:
                    return cur_x - 1, cur_y, next_pipe.connected_directions[1]
                elif Pipe.Direction.EAST == next_pipe.connected_directions[1]:
                    return cur_x - 1, cur_y, next_pipe.connected_directions[0]
                return None

    def parse_and_analyze_loop(self) -> int:
        """
        find the loop, while registering the amount of steps it took to reach the field
        :returns: the maximum amount of steps required
        """
        # try every option for connected directions for starting field
        for direction in Pipe.Direction:
            # reset map
            steps_taken_map: list[list[int]] = [[0 for _ in range(len(self.pipes[0]))] for _ in range(len(self.pipes))]
            cur_steps_taken = 0
            cur_x = self.starting_coordinates[0]
            cur_y = self.starting_coordinates[1]
            cur_direction = direction
            # walk the loop in one direction, while registering amount of steps
            # if first step is not possible, go to next
            step_result = self._get_next_pipe_coordinates_and_direction(cur_x, cur_y, cur_direction)
            if not step_result:
                continue
            # walk first step
            cur_x, cur_y, cur_direction = step_result
            cur_steps_taken += 1
            # walk steps until we reach the beginning
            while not (cur_x == self.starting_coordinates[0] and cur_y == self.starting_coordinates[1]):
                # register amount of steps to reach this point
                steps_taken_map[cur_x][cur_y] = cur_steps_taken
                # print(f"Walking from ({cur_x}, {cur_y}) in direction {cur_direction}.")
                step_result = self._get_next_pipe_coordinates_and_direction(cur_x, cur_y, cur_direction)
                # check if next step is impossible:
                if not step_result:
                    break
                # walk next step
                last_walked_direction = cur_direction
                cur_x, cur_y, cur_direction = step_result
                # print(f"Walked to ({cur_x}, {cur_y}). Next direction: {cur_direction}")
                cur_steps_taken += 1
            else:
                # no impossible step was reached, loop fully completed
                # walk loop the other direction, to find minimal steps for each field
                cur_steps_taken = 0
                cur_x = self.starting_coordinates[0]
                cur_y = self.starting_coordinates[1]
                # get inverse of last walked direction to walk the other way
                match last_walked_direction:
                    case Pipe.Direction.NORTH:
                        cur_direction = Pipe.Direction.SOUTH
                    case Pipe.Direction.EAST:
                        cur_direction = Pipe.Direction.WEST
                    case Pipe.Direction.SOUTH:
                        cur_direction = Pipe.Direction.NORTH
                    case Pipe.Direction.WEST:
                        cur_direction = Pipe.Direction.EAST
                # walk as long as the current field used more steps during the first walkthrough
                while steps_taken_map[cur_x][cur_y] >= cur_steps_taken:  # >= to not stop for starting position
                    # reduce steps to the amount we needed in the other direction
                    steps_taken_map[cur_x][cur_y] = cur_steps_taken
                    # go to next field
                    # we don't expect None here, as we already confirmed the loop works.
                    cur_x, cur_y, cur_direction = \
                        self._get_next_pipe_coordinates_and_direction(cur_x, cur_y, cur_direction)
                    cur_steps_taken += 1
                return max(max(points_x) for points_x in steps_taken_map)

        # error state
        raise Exception('No full loop was found.')


def one(in_lines: list[str]) -> int:
    pipe_game = PipeGame(in_lines)
    return pipe_game.parse_and_analyze_loop()


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_lines = f.readlines()
    print(one(input_lines))
