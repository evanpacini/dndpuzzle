import random as rd
import numpy as np
from itertools import combinations


def comp_col(grid):
    return np.vectorize(lambda x: x >> 1)(grid).sum(axis=0)


def comp_row(grid):
    return np.vectorize(lambda x: x >> 1)(grid).sum(axis=1)


def comp_stars(grid, uncovered_stars=False):
    return np.count_nonzero(grid == 1) if uncovered_stars else np.count_nonzero(grid == 3)


def check_col(grid, col_amounts):
    return np.array_equal(comp_col(grid), col_amounts)


def check_row(grid, row_amounts):
    return np.array_equal(comp_row(grid), row_amounts)


def check_stars(grid, stars, uncovered_stars=False):
    return comp_stars(grid, uncovered_stars) == stars


def check_conditions(grid, row_amounts, col_amounts, stars, uncovered_stars=False):
    return (check_row(grid, row_amounts)
            and check_col(grid, col_amounts)
            and check_stars(grid, stars, uncovered_stars))


def is_valid_move(grid, row_amounts, col_amounts, stars, row, col, uncovered_stars=False):
    covered = comp_stars(grid, uncovered_stars) + (grid[row][col] & 1) * (-1 if uncovered_stars else 1)
    return (grid[row][col] < 2
            and comp_row(grid)[row] < row_amounts[row]
            and comp_col(grid)[col] < col_amounts[col]
            and (covered >= stars if uncovered_stars else covered <= stars))


def solve_shuffled(grid, row_amounts, col_amounts, stars, uncovered_stars=False):
    global solutions
    if check_conditions(grid, row_amounts, col_amounts, stars):
        if not is_grid_in_solutions(grid):
            solutions = np.append(solutions, [grid], axis=0)
            print("\nSolution:")
            print_grid(grid)
        return True

    for i, j in rd.sample([(i, j) for i in range(len(grid)) for j in range(len(grid[0]))], len(grid) * len(grid[0])):
        if is_valid_move(grid, row_amounts, col_amounts, stars, i, j, uncovered_stars):
            grid[i][j] |= 2

            if solve_shuffled(grid, row_amounts, col_amounts, stars, uncovered_stars):
                return True

            grid[i][j] &= 1

    return False


def print_grid(grid):
    for row in grid:
        for cell in row:
            match cell:
                case 0:
                    print(" ", end=" ")
                case 1:
                    print("*", end=" ")
                case 2:
                    print("O", end=" ")
                case 3:
                    print("@", end=" ")
        print()


def is_grid_in_solutions(grid):
    global solutions
    for solution in solutions:
        if np.array_equal(grid, solution):
            return True
    return False


def solve_combinations(grid, row_amounts, col_amounts, stars, uncovered_stars=False):
    global solutions

    skull_position_combinations = list(combinations(range(len(grid) * len(grid[0])), 9))
    print("Number of combinations:", len(skull_position_combinations))

    for i, combination in enumerate(skull_position_combinations):
        print(f"Percentage: {round(i / len(skull_position_combinations) * 100, 2)}%", end="\r")
        new_grid = grid.copy()
        for skull in combination:
            new_grid[skull // len(grid)][skull % len(grid[0])] |= 2

        if check_conditions(new_grid, row_amounts, col_amounts, stars, uncovered_stars):
            if not is_grid_in_solutions(new_grid):
                solutions = np.append(solutions, [new_grid], axis=0)
                print("\nSolution:")
                print_grid(new_grid)


def main():
    # 0 = empty, 1 = star, 2 = skull, 3 = skull & star
    grid = np.array([[1, 0, 0, 1],
                     [0, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 1, 0]])

    row_amounts = np.array([3, 2, 3, 1])
    col_amounts = np.array([3, 1, 2, 3])
    stars = 4
    uncovered_stars = False
    #
    # while True:
    #     print("Solving...")
    #     solve_shuffled(grid.copy(), row_amounts, col_amounts, stars, uncovered_stars)
    solve_combinations(grid.copy(), row_amounts, col_amounts, stars, uncovered_stars)


solutions = np.empty((0, 4, 4), dtype=int)

if __name__ == "__main__":
    main()
