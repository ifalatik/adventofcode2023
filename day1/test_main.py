import unittest
import main


class TestMain(unittest.TestCase):
    test_input_lines_one: list[str]
    test_input_lines_two: list[str]

    @classmethod
    def setUpClass(cls) -> None:
        with open('test_input_one.txt', 'r') as f:
            cls.test_input_lines_one = f.readlines()
        with open('test_input_two.txt', 'r') as f:
            cls.test_input_lines_two = f.readlines()

    def test_get_calibration_value(self):
        expected_results = [12, 38, 15, 77]
        for idx, line in enumerate(TestMain.test_input_lines_one):
            self.assertEqual(expected_results[idx], main.get_calibration_value(line))

    def test_one(self):
        self.assertEqual(142, main.one(TestMain.test_input_lines_one))

    def test_to_int(self):
        test_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        for i in range(1, 10):
            self.assertEqual(i, main.to_int(str(i)))
            self.assertEqual(i, main.to_int(test_strings[i-1]))

    def test_get_calibration_value_with_test(self):
        expected_results = [29, 83, 13, 24, 42, 14, 76, 28]
        for idx, line in enumerate(TestMain.test_input_lines_two):
            self.assertEqual(expected_results[idx], main.get_calibration_value_with_text(line))

    def test_two(self):
        self.assertEqual(281, main.two(TestMain.test_input_lines_two))


if __name__ == '__main__':
    unittest.main()
