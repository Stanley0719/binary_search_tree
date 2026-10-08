import unittest

from bst import BinarySearchTree, parse_sequence


class ParseSequenceTests(unittest.TestCase):
    def test_accepts_commas_and_whitespace(self) -> None:
        self.assertEqual(parse_sequence("8, 3\t10\n1"), [8, 3, 10, 1])

    def test_rejects_empty_sequence(self) -> None:
        with self.assertRaisesRegex(ValueError, "至少一個整數"):
            parse_sequence(" ,  \n")

    def test_rejects_non_integer_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "只能包含整數"):
            parse_sequence("8, nope, 3")


class BinarySearchTreeTests(unittest.TestCase):
    def test_inserts_nodes_and_records_their_routes(self) -> None:
        tree = BinarySearchTree()
        insertions = [tree.insert(value) for value in [8, 3, 10, 6, 4]]

        self.assertEqual([node.value for node in tree.nodes_in_order()], [3, 4, 6, 8, 10])
        self.assertEqual(
            [node.value for node in insertions[-1].route],
            [8, 3, 6, 4],
        )
        self.assertEqual(insertions[-1].directions, ["左", "右", "左"])
        self.assertEqual(insertions[-1].node.depth, 3)

    def test_places_duplicate_values_on_the_right(self) -> None:
        tree = BinarySearchTree()
        tree.insert(5)
        duplicate = tree.insert(5)

        self.assertIs(tree.root.right, duplicate.node)
        self.assertEqual(duplicate.directions, ["右"])


if __name__ == "__main__":
    unittest.main()
