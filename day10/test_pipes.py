import unittest
import pipes


class TestPipeGame(unittest.TestCase):
    test_input_lines_one: list[str]
    test_input_lines_two: list[str]

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        with open('test_input_one.txt', 'r') as f:
            cls.test_input_lines_one = f.readlines()
        with open('test_input_two.txt') as f:
            cls.test_input_lines_two = f.readlines()

    @classmethod
    def tearDownClass(cls) -> None:
        """This teardown will only be executed once after all tests are done"""

    pass

    def test_parse_and_analyze_loop(self):
        pipe_game = pipes.PipeGame(TestPipeGame.test_input_lines_one)
        self.assertEqual([
            [0, 0, 0, 1, 2],
            [0, 2, 1, 4, 3],
            [4, 3, 0, 5, 0],
            [5, 6, 7, 6, 0],
            [0, 0, 8, 7, 0]],
            pipe_game.parse_and_analyze_loop())

    def test_one(self):
        self.assertEqual(8, pipes.one(TestPipeGame.test_input_lines_one))

    def test_two(self):
        self.assertEqual(10, pipes.two(TestPipeGame.test_input_lines_two))


if __name__ == '__main__':
    unittest.main()
