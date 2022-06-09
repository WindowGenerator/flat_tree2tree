import unittest

from main import to_tree, ParseTreeError


class TestToTree(unittest.TestCase):
    def test_simple(self) -> None:
        source = [
            (None, 'a'),
            (None, 'b'),
            (None, 'c'),
            ('a', 'a1'),
            ('a', 'a2'),
            ('a2', 'a21'),
            ('a2', 'a22'),
            ('b', 'b1'),
            ('b1', 'b11'),
            ('b11', 'b111'),
            ('b', 'b2'),
            ('c', 'c1'),
        ]

        expected = {
            'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
            'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
            'c': {'c1': {}},
        }

        assert to_tree(source) == expected

    def test_not_sorted_tree(self) -> None:
        source = [
            (None, 'c'),
            ('a', 'a1'),
            ('a2', 'a22'),
            ('b', 'b2'),
            (None, 'a'),
            ('a', 'a2'),
            ('b', 'b1'),
            (None, 'b'),
            ('b1', 'b11'),
            ('b11', 'b111'),
            ('a2', 'a21'),
            ('c', 'c1'),
        ]

        expected = {
            'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
            'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
            'c': {'c1': {}},
        }

        assert to_tree(source) == expected
    
    def test_similar_references_on_child(self) -> None:
        source = [
            (None, 'a'),
            (None, 'b'),
            ('a', 'fail'),
            ('b', 'fail'),
        ]
        self.assertRaises(ParseTreeError, to_tree, source)

    def test_not_exist_node_in_tree(self) -> None:
        source = [
            (None, 'a'),
            ('a', 'c'),
            ('b', 'fail'),
        ]
        self.assertRaises(ParseTreeError, to_tree, source)


if __name__ == "__main__":
    unittest.main()