import unittest
import cube_game

from unittest.mock import patch


class TestTemplate(unittest.TestCase):
    test_input_lines: list[str]

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        with open('test_input.txt', 'r') as f:
            cls.test_input_lines = f.readlines()

    pass

    @classmethod
    def tearDownClass(cls) -> None:
        """This teardown will only be executed once after all tests are done"""

    pass

    def test_get_max_for_color(self):
        gr = cube_game.GameRound(TestTemplate.test_input_lines[0])
        self.assertEqual(6, gr.get_max_for_color(cube_game.Color.blue))
        self.assertEqual(4, gr.get_max_for_color(cube_game.Color.red))
        self.assertEqual(2, gr.get_max_for_color(cube_game.Color.green))
        gr = cube_game.GameRound(TestTemplate.test_input_lines[1])
        self.assertEqual(4, gr.get_max_for_color(cube_game.Color.blue))
        self.assertEqual(1, gr.get_max_for_color(cube_game.Color.red))
        self.assertEqual(3, gr.get_max_for_color(cube_game.Color.green))

    def test_one(self):
        self.assertEqual(8, cube_game.one(TestTemplate.test_input_lines))

    def test_two(self):
        self.assertEqual(2286, cube_game.two(TestTemplate.test_input_lines))


if __name__ == '__main__':
    unittest.main()
