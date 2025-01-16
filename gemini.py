import random


def is_valid(grid: list[list[int]], row: int, col: int, num: int) -> bool:
    """Checks if placing 'num' at (row, col) is valid in the Sudoku grid."""
    # Check row
    if num in grid[row]:
        return False

    # Check column
    if num in [grid[i][col] for i in range(9)]:
        return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(grid: list[list[int]]) -> bool:
    """Solves a Sudoku puzzle using backtracking."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):  # Recursive call
                            return True
                        grid[row][col] = 0  # Backtrack
                return False  # No solution found
    return True  # Puzzle is filled


def generate_sudoku(difficulty: int = 30) -> list[list[int]]:
    """Generates a Sudoku puzzle with a given difficulty (number of empty cells)."""

    # Create a solved Sudoku grid
    grid: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
    # Fill the diagonal boxes to start with a valid grid that is easier to solve
    for i in range(0, 9, 3):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for j in range(3):
            for k in range(3):
                grid[i + j][i + k] = numbers.pop()

    solve_sudoku(grid)

    # Remove numbers to create the puzzle
    num_to_remove = 81 - difficulty  # Target number of filled cells
    while num_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            num_to_remove -= 1

    return grid


def print_grid(grid: list[list[int]]) -> None:
    """Prints the Sudoku grid in a user-friendly format."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j], end=" ")
        print()


# Example usage:
puzzle = generate_sudoku(
    difficulty=30
)  # Adjust difficulty here. Lower number means more difficult.
print("Sudoku Puzzle:")
print_grid(puzzle)


# To check the solution:
solved_puzzle = [row[:] for row in puzzle]  # Create a copy
solve_sudoku(solved_puzzle)
print("\nSolution:")
print_grid(solved_puzzle)
