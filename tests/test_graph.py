import os
import unittest

from src.errors import RepositoryError
from src.graph import build_graph, find_cycles, load_order
from src.local_repo import LocalRepository, parse_graph


def repo(name):
    return LocalRepository(os.path.join("tests", "data", name))


class LocalRepositoryTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_graph("A: B C\nB:"), {"A": ["B", "C"], "B": []})

    def test_lowercase_name(self):
        with self.assertRaises(RepositoryError):
            parse_graph("A: b")

    def test_bad_line(self):
        with self.assertRaises(RepositoryError):
            parse_graph("A B")

    def test_missing_file(self):
        with self.assertRaises(RepositoryError):
            LocalRepository("no_such_file.txt")

    def test_unknown_package(self):
        with self.assertRaises(RepositoryError):
            repo("simple.txt").dependencies("Z")


class BuildGraphTest(unittest.TestCase):
    def test_full_graph(self):
        graph = build_graph(repo("simple.txt"), "A", 10)
        self.assertEqual(list(graph), ["A", "B", "C", "D", "E", "F"])
        self.assertEqual(graph["C"], ["D", "E"])

    def test_depth(self):
        graph = build_graph(repo("simple.txt"), "A", 1)
        self.assertEqual(graph, {"A": ["B", "C"], "B": [], "C": []})

    def test_exclude(self):
        graph = build_graph(repo("deep.txt"), "A", 10, "X")
        self.assertNotIn("X", graph)
        self.assertNotIn("XY", graph)
        self.assertIn("E", graph)

    def test_cycle(self):
        graph = build_graph(repo("cycle.txt"), "A", 10)
        self.assertEqual(graph["C"], ["A", "D"])
        self.assertEqual(find_cycles(graph), [["A", "B", "C", "A"]])

    def test_no_cycles(self):
        graph = build_graph(repo("simple.txt"), "A", 10)
        self.assertEqual(find_cycles(graph), [])


class LoadOrderTest(unittest.TestCase):
    def test_order(self):
        graph = build_graph(repo("simple.txt"), "A", 10)
        order, rest = load_order(graph)
        self.assertEqual(order, ["E", "F", "D", "B", "C", "A"])
        self.assertEqual(rest, [])

    def test_order_with_cycle(self):
        graph = build_graph(repo("cycle.txt"), "A", 10)
        order, rest = load_order(graph)
        self.assertEqual(order, ["D"])
        self.assertEqual(rest, ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
