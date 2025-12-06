import unittest

class TestPortfolio(unittest.TestCase):
    def test_math(self):
        # Простий тест, щоб перевірити, чи працює pre-push hook
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()