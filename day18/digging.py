class DigSite:
    _min_x: int = 0
    _min_y: int = 0
    _points: list[tuple[int, int]] = []


    def _add_move(self, direction: str, steps: int):


    def __init__(self, moves: list[str]):
        self.Digger = DigSite.Digger()
        for move in moves:

    class Digger:
        _x: int = 0
        _y: int = 0

    @staticmethod
    def _get_next_position(x: int, y: int, direction: str, steps: int) -> tuple[int, int]:
        match direction:
            case 'R':
                return x + steps, y
            case 'D':
                return x, y + steps
            case 'L':
                return x - steps, y
            case 'U':
                return x, y - steps

    @staticmethod
    def _color_str_to_int(col_str: str) -> int:
        return int(col_str[2:-1], base=16)

    def get_volume(self) -> int:
        pass


def one(in_lines: list[str]) -> int:
    digger = Digger(in_lines)
    print(digger.get_visited_positions())
    return digger.get_volume()


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_lines = f.readlines()
    print(one(input_lines))
