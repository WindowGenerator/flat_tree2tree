from typing import List, Dict, Tuple, Optional
from itertools import chain


FlatNode = Tuple[Optional[str], str]


class ParseTreeError(Exception):
    pass


def _to_tree(flat_tree: List[FlatNode]) -> Dict:
    """
    Space complexity: O(n)
    Time complexity: O(n)
    """
    tree = {}

    for parent, child in flat_tree:
        if parent is not None:
            if parent not in tree:
                tree[parent] = {}

            if child not in tree:
                tree[parent][child] = {}
                tree[child] = tree[parent][child]
            else:
                tree[parent][child] = tree[child]


    for parent, child in flat_tree:
        if parent is not None and child in tree:
            del tree[child]
    
    return tree


def _check_similar_references_on_child(flat_tree: List[FlatNode]) -> None:
    children = set()
    for _, child in flat_tree:
        if child in children:
            raise ParseTreeError(f"Multiple parents refer to the same child: '{child}'")
        else:
            children.add(child)


def _check_not_exist_node_in_tree(tree: Dict, flat_tree: List[FlatNode]) -> None:
    nodes = [tree]
    nodes_count = 0

    while nodes:
        node = nodes.pop()

        for _, child_node in node.items():
            nodes_count += 1
            nodes.append(child_node)
    
    if nodes_count != len(flat_tree):
        raise ParseTreeError("The data structure is not a tree")


def to_tree(flat_tree: List[FlatNode]) -> Dict:
    _check_similar_references_on_child(flat_tree)

    tree = _to_tree(flat_tree)

    _check_not_exist_node_in_tree(tree, flat_tree)

    return tree
