from copy import deepcopy

import numpy as np


class Cell:
    def __init__(self, value, potential_values, x, y):
        self.value = value
        self.potential_values = potential_values
        self.x = x
        self.y = y

    def update_cell(self, grid):
        changed = False
        works = True
        things_to_remove = set()
        cells_to_check = []
        row = grid[self.x]
        cells_to_check.extend(row)
        column = grid[:, self.y]
        cells_to_check.extend(column)
        top_of_box = self.x - (self.x % 3)
        left_of_box = self.y - (self.y % 3)
        box = grid[top_of_box:top_of_box+3, left_of_box:left_of_box+3]
        box = box.flatten()
        cells_to_check.extend(box)
        for cell in cells_to_check:
            if cell.value != 0 and cell.value in self.potential_values:
                things_to_remove.add(cell.value)
        if len(things_to_remove) > 0:
            changed = True

        for thing_to_remove in things_to_remove:
            self.potential_values.remove(thing_to_remove)

        if self.value == 0 and len(self.potential_values) == 0:
            works = False

        if len(self.potential_values) == 1:
            self.value = self.potential_values[0]
            self.potential_values = []
        else:
            for value in self.potential_values:
                only_possible_place = [True, True, True]
                for cell in row:
                    if not(cell.x == self.x and cell.y == self.y) and value in cell.potential_values:
                        only_possible_place[0] = False
                for cell in column:
                    if not(cell.x == self.x and cell.y == self.y) and value in cell.potential_values:
                        only_possible_place[1] = False
                for cell in box:
                    if not(cell.x == self.x and cell.y == self.y) and value in cell.potential_values:
                        only_possible_place[2] = False
                if any(only_possible_place):
                    self.value = value
                    self.potential_values = []
                    changed = True
        return changed, works

    def check_if_cell_can_have_value(self, grid, value):
        cells_to_check = []
        row = grid[self.x]
        cells_to_check.extend(row)
        column = grid[:, self.y]
        cells_to_check.extend(column)
        top_of_box = self.x - (self.x % 3)
        left_of_box = self.y - (self.y % 3)
        box = grid[top_of_box:top_of_box + 3, left_of_box:left_of_box + 3]
        box = box.flatten()
        cells_to_check.extend(box)
        for cell in cells_to_check:
            if cell.value == value:
                return False
        return True


def is_finished(grid):
    for x in range(9):
        for y in range(9):
            if grid[x, y].value == 0:
                return False
    return True


def evaluate_grid(grid):
    time_since_last_change = 0
    while not is_finished(grid):
        changed_grid = False
        for x in range(9):
            for y in range(9):
                if grid[x, y].value == 0:
                    changed, works = grid[x, y].update_cell(grid)
                    l = grid[x, y].potential_values
                    if not works:
                        return None
                    if changed:
                        changed_grid = True
        if not changed_grid:
            time_since_last_change += 1
        if time_since_last_change == 3:
            done = False
            for x in range(9):
                for y in range(9):
                    if len(grid[x, y].potential_values) > 0:
                        done = True
                        for value in grid[x, y].potential_values:
                            if grid[x, y].check_if_cell_can_have_value(grid, value):
                                new_grid = deepcopy(grid)
                                new_grid[x, y].value = value
                                new_grid[x, y].potential_values = []
                                evaluated_grid = evaluate_grid(new_grid)
                                if evaluated_grid is not None:
                                    grid = evaluated_grid
                                time_since_last_change = 0
                    if done:
                        break
                if done:
                    break
    return grid


