import json

from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
#from solver import Cell, evaluate_grid

# Create your views here.
from sudoku.solver import Cell, evaluate_grid


def index(request):
    return render(request, 'sudoku/grid.html')


def test_example(request):
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
    grid = {}
    letters = list("ABCDEFGHI")
    for row in range(9):
        for column in range(9):
            grid[letters[row] + str(column)] = test_grid[row][column]
    context = {'grid': grid}
    return render(request, 'sudoku/grid.html', context)


def solve(request):
    grid = np.empty((9, 9), dtype=Cell)
    letters = list("ABCDEFGHI")
    for row in range(9):
        for column in range(9):
            i = request.POST[letters[row] + str(column)]
            v = int(i) if len(i) > 0 else 0
            grid[row, column] = Cell(v, ([1, 2, 3, 4, 5, 6, 7, 8, 9] if v == 0 else []), row, column)
    solved = evaluate_grid(grid)
    """
    solved_grid = []
    for r in range(9):
        row = []
        for c in range(9):
            row.append(solved[r][c].value)
        solved_grid.append(row)
    """
    grid = {}
    letters = list("ABCDEFGHI")
    for row in range(9):
        for column in range(9):
            grid[letters[row]+str(column)] = solved[row][column].value
    context = {'grid': grid}
    return render(request, 'sudoku/grid.html', context)
