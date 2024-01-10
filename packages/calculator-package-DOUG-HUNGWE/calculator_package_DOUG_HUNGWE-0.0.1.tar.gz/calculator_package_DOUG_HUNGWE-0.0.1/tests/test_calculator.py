import unittest
# Import the Calculator class from calculator module
from calculator import Calculator


class TestCalc(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()  # Create an instance of the Calculator class for testing

    def test_add(self):
        self.assertEqual(self.calc.add(2), 2)
        self.assertEqual(self.calc.add(5, 2), 7)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(self.calc.add(2), 2)
        self.assertEqual(self.calc.subtract(5, 2), 3)
        self.assertEqual(self.calc.subtract(-1, 1), -2)
        self.assertEqual(self.calc.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(2, 2), 4)
        self.assertEqual(self.calc.multiply(-1, 1), -1)
        self.assertEqual(self.calc.multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 5), 2)
        self.assertEqual(self.calc.divide(-1, 1), -1)
        self.assertEqual(self.calc.divide(-1, -1), 1)
        self.assertEqual(self.calc.divide(3, 2), 1.5)

        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_nth_root(self):
        # Cube root of 8 is 2.0
        self.assertEqual(self.calc.nth_root(8, 3), 2.0)
        self.assertEqual(self.calc.nth_root(16, 4),
                         2.0)  # 4th root of 16 is 2.0
        # Cube root of 27 is 3.0
        self.assertEqual(self.calc.nth_root(27, 3), 3.0)

        with self.assertRaises(ValueError):
            # Attempting to calculate the square root of a negative number should raise an exception
            self.calc.nth_root(-4, 2)


if __name__ == '__main__':
    unittest.main()
