import unittest

from src.d2 import to_d2


class D2Test(unittest.TestCase):
    def test_edges(self):
        text = to_d2({"A": ["B"], "B": []})
        self.assertIn('"A" -> "B"', text)
        self.assertTrue(text.startswith("direction: down"))

    def test_single_node(self):
        self.assertIn('"A"', to_d2({"A": []}))


if __name__ == "__main__":
    unittest.main()
