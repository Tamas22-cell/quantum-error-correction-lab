import unittest
from main import logical_error_uncoded, logical_error_encoded


class TestBitFlipCode(unittest.TestCase):
    def test_zero_noise(self):
        self.assertEqual(logical_error_encoded(0), 0)

    def test_half_noise(self):
        self.assertAlmostEqual(logical_error_encoded(0.5), 0.5)

    def test_improvement_at_ten_percent(self):
        self.assertAlmostEqual(logical_error_encoded(0.1), 0.028)
        self.assertLess(logical_error_encoded(0.1), logical_error_uncoded(0.1))

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            logical_error_encoded(-0.1)


if __name__ == '__main__':
    unittest.main()
