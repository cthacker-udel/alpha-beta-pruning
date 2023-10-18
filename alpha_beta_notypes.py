from unittest import TestCase


tests = [["2 4 13 11 1 3 3 7 3 3 2 2", "3 6 7 10 11"], [
    "1 4 2 6 8 7 3 7 2 3 2 2", "10 11"], ["15 4 12 16 10 7 3 1 2 3 2 2", "6 7 10 11"], ["1 4 12 16 1 7 3 1 2 8 2 2", "3"], ["1 4 12 16 1 7 3 1 2 8 10 2", "3 11"]]


class TreeNode:
    """
    Represents a node in the tree, contains all necessary fields to execute alpha-beta pruning
    """

    def __init__(self, is_min, value=None, is_leaf=False, index=None):
        """
        The initializer for the TreeNode class, contains all integral fields for a tree node

        Args:
            self (TreeNode): The internal TreeNode instance
            is_min (bool): Whether the node is a minimizer
            value (Optional[int  |  float], optional): The value of the tree node. Defaults to None.
            is_leaf (bool, optional): Whether the node is a leaf node. Defaults to False.
            index (_type_, optional): The index of the tree node (used for output). Defaults to None.
        """
        self.children = []  # Left to right
        self.is_min = is_min
        self.value = value if value is not None else float(
            'inf') if is_min else float('-inf')
        self.is_leaf = is_leaf
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.index = index if index is not None else -1


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

    def __init__(self, nodes) -> None:
        """
        Initializes the Tree enabled with Alpha-Beta pruning capabilities

        Args:
            self (AlphaBetaPruning): The internal AlphaBetaPruning instance
            nodes (List[int]): The nodes initialized within the tree

        Raises:
            ValueError: If the supplied node length is not == 12 (which is it hard-coded to process)
        """

        if len(nodes) != 12:
            raise ValueError("Must supply valid node length = 12")

        self.root_node = TreeNode(False)
        self.root_node.children = [
            TreeNode(True), TreeNode(True), TreeNode(True)]
        self.explored_indexes = set()
        self.theoretical_range = set(range(0, len(nodes)))

        ind = 0
        for each_child in self.root_node.children:
            left_max = TreeNode(False)
            right_max = TreeNode(False)
            each_child.children = [left_max, right_max]

            left_max.children += [TreeNode(False, nodes[ind], True, ind)]
            ind += 1
            left_max.children += [TreeNode(False, nodes[ind], True, ind)]
            ind += 1

            right_max.children += [TreeNode(False, nodes[ind], True, ind)]
            ind += 1
            right_max.children += [TreeNode(False, nodes[ind], True, ind)]
            ind += 1

    def run_traversal(self, curr_node=None, alpha=None, beta=None) -> None:
        """
        Runs the traversal of the tree, with alpha-beta pruning enabled

        Args:
            self (AlphaBetaPruning): The internal AlphaBetaPruning class instance
            curr_node (Optional[TreeNode], optional): The current node the algorithm is on, used for recursive data to be passed. Defaults to None.
            alpha (Optional[float  |  int], optional): The alpha of the child node, used for recursive data to be passed. Defaults to None.
            beta (Optional[float  |  int], optional): The beta of the child node, used for recursive data to be passed. Defaults to None.

        Returns:
            _type_: Nothing, since it internally updated explored indexes
        """
        if curr_node.is_leaf:
            self.explored_indexes.add(curr_node.index)
            return curr_node.value

        curr_node.alpha = alpha if alpha is not None else curr_node.alpha
        curr_node.beta = beta if beta is not None else curr_node.beta

        if curr_node.is_min:
            computed_value = curr_node.value
            for each_child in curr_node.children:
                computed_value = min(
                    computed_value, self.run_traversal(each_child, curr_node.alpha, curr_node.beta))
                if computed_value <= curr_node.alpha:
                    return computed_value
                curr_node.beta = computed_value

            return computed_value
        else:
            computed_value = curr_node.value
            for each_child in curr_node.children:
                computed_value = max(
                    computed_value, self.run_traversal(each_child, curr_node.alpha, curr_node.beta))
                if computed_value >= curr_node.beta:
                    return computed_value
                curr_node.alpha = computed_value

            return computed_value


def main(run_input=True):
    """
    The main loop, contains a boolean denoting whether to process the user input

    Args:
        run_input (bool, optional): Whether to process user input when running. Defaults to False.
    """
    if run_input:
        inp = input()
        solver = AlphaBetaPruning([int(x)
                                   for x in inp.split(' ')])
        solver.run_traversal(solver.root_node)
        pruned_nodes = ' '.join([str(x) for x in sorted(
            solver.theoretical_range.difference(solver.explored_indexes))])
        print(pruned_nodes)
    else:
        evaluator = TestCase()
        for ind, each_test in enumerate(tests):
            solver = AlphaBetaPruning([int(x)
                                      for x in each_test[0].split(' ')])
            solver.run_traversal(solver.root_node)
            pruned_nodes = ' '.join([str(x) for x in sorted(
                solver.theoretical_range.difference(solver.explored_indexes))])
            evaluator.assertEqual(pruned_nodes, each_test[1])
            print(f"-------------- TEST {ind} PASSED --------------")


if __name__ == '__main__':
    main()
