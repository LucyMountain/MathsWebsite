import unittest

import numpy as np

from sudoku.solver import evaluate_grid, Cell


class MyTestCase(unittest.TestCase):
    def test_sudoku_solver(self):
        grid = np.empty((9, 9), dtype=Cell)

        test_grid = [
            [9, 0, 1, 0, 0, 5, 4, 8, 0],
            [0, 0, 0, 2, 0, 0, 0, 7, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 6, 0, 0, 9, 1, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 9],
            [6, 0, 8, 0, 7, 0, 0, 4, 0],
            [0, 5, 0, 0, 0, 0, 8, 0, 0],
            [0, 3, 0, 0, 0, 6, 0, 0, 0]
        ]

        for row in range(9):
            for column in range(9):
                v = test_grid[row][column]
                grid[row, column] = Cell(v, ([1, 2, 3, 4, 5, 6, 7, 8, 9] if v == 0 else []), row, column)
        solved = evaluate_grid(grid)

        for row in range(9):
            for column in range(9):
                self.assertTrue(solved[row][column].value > 0)


if __name__ == '__main__':
    unittest.main()
