from __future__ import annotations
from unittest import TestCase
from typing import List, Optional


tests = [["2 4 13 11 1 3 3 7 3 3 2 2", "3 6 7 10 11"], [
    "1 4 2 6 8 7 3 7 2 3 2 2", "10 11"], ["15 4 12 16 10 7 3 1 2 3 2 2", "6 7 10 11"]]


class TreeNode:
    def __init__(self: TreeNode, is_min: bool, value: Optional[int | float] = None, is_leaf: bool = False) -> None:
        self.children: List[TreeNode] = []  # Left to right
        self.is_min = is_min
        self.value = value if value is not None else float(
            'inf') if is_min else float('-inf')
        self.is_leaf = is_leaf
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.explored: bool = False

    def explore(self: TreeNode) -> None:
        self.explored = True


class AlphaBetaPruning:
    """
    Represents a class that processes the 12 terminal nodes of the tree

                            MIN
                             |
                    --------------------
                    |        |         |
                   MAX      MAX       MAX
                    |        |         |
                   ---      ---       ---
                  /   \    /   \     /   \
                 MIN  MIN MIN  MIN  MIN  MIN
                /   \/   \/  \/   \/   \/   \ 
               o    oo   oo  oo   oo   oo    o
    """

    def __init__(self: AlphaBetaPruning, nodes: List[int]) -> None:

        if len(nodes) != 12:
            raise ValueError("Must supply valid node length = 12")

        self.root_node = TreeNode(False)
        self.root_node.children = [
            TreeNode(True), TreeNode(True), TreeNode(True)]

        ind = 0
        for each_child in self.root_node.children:
            left_max = TreeNode(False)
            right_max = TreeNode(False)
            each_child.children = [left_max, right_max]

            left_max.children = [TreeNode(False, nodes[ind], True)]
            ind += 1
            left_max.children = [TreeNode(False, nodes[ind], True)]
            ind += 1

            right_max.children = [TreeNode(False, nodes[ind], True)]
            ind += 1
            right_max.children = [TreeNode(False, nodes[ind], True)]
            ind += 1

    def run_traversal(self: AlphaBetaPruning, curr_node: Optional[TreeNode] = None) -> None:
        if curr_node.is_leaf:
            return curr_node.value
        elif curr_node.is_min:
            computed_value = curr_node.value
            for each_child in curr_node.children:
                computed_value = min(
                    computed_value, self.run_traversal(each_child))
            if computed_value > curr_node.beta:
                return computed_value
        else:
            computed_value = curr_node.value
            for each_child in curr_node.children:
                computed_value = max(
                    computed_value, self.run_traversal(each_child))
            if computed_value < curr_node.alpha:
                return computed_value


def main(run_input=False):
    """
    The main loop, contains a boolean denoting whether to process the user input

    Args:
        run_input (bool, optional): Whether to process user input when running. Defaults to False.
    """
    if run_input:
        pass
    else:
        evaluator = TestCase()
        for each_test in tests:
            solver = AlphaBetaPruning([int(x)
                                      for x in each_test[0].split(' ')])
            result = solver.run_traversal(solver.root_node)


if __name__ == '__main__':
    main()
