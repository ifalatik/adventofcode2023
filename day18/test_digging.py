import unittest
import digging

from unittest.mock import patch


class TestDigging(unittest.TestCase):
    test_input_lines: list[str]

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        with open('test_input.txt', 'r') as f:
            cls.test_input_lines = f.readlines()

    @classmethod
    def tearDownClass(cls) -> None:
        """This teardown will only be executed once after all tests are done"""

    pass

    def test_one(self):
        self.assertEqual(46, digging.one(TestDigging.test_input_lines))

    @unittest.skip
    def test_two(self):
        self.assertEqual(51, digging.two(TestDigging.test_input_lines))


if __name__ == '__main__':
    unittest.main()
