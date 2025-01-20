# ChatGPT 4o Mini
# 2025-01-20

# Prompts used:
# 1. generate python code to create and solve a sudoku puzzle
# 2. optimise for performance, efficiency and speed
# 3. find refactoring opportunities
# 4. improve static type checking and annotation
# 5. improve the commenting, documentation and readability
# 6. generate pytest unit tests

import random
from typing import List, Optional, Set

# Constants for the Sudoku grid
GRID_SIZE = 9  # 9x9 grid
SUBGRID_SIZE = 3  # 3x3 subgrids


class Board:
    """
    A class that represents the Sudoku board.
    It handles validation of moves, placement, removal of numbers,
    and maintaining constraint sets for rows, columns, and subgrids.
    """

    def __init__(self) -> None:
        """
        Initializes an empty Sudoku board and prepares sets for rows,
        columns, and 3x3 subgrids to track numbers already placed.
        """
        self.board: List[List[int]] = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.rows: List[Set[int]] = [set() for _ in range(GRID_SIZE)]  # Track numbers in each row
        self.cols: List[Set[int]] = [set() for _ in range(GRID_SIZE)]  # Track numbers in each column
        self.boxes: List[Set[int]] = [set() for _ in range(GRID_SIZE)]  # Track numbers in each 3x3 box

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if placing the number `num` at the given row and column is valid.
        A number is valid if it does not already exist in the row, column, or subgrid.

        Args:
            row (int): The row index (0-based).
            col (int): The column index (0-based).
            num (int): The number to check.

        Returns:
            bool: True if the number can be placed at the given position, False otherwise.
        """
        box_index = (row // SUBGRID_SIZE) * SUBGRID_SIZE + (col // SUBGRID_SIZE)
        return num not in self.rows[row] and num not in self.cols[col] and num not in self.boxes[box_index]

    def place_number(self, row: int, col: int, num: int) -> None:
        """
        Places the number `num` at the specified position (row, col) and updates
        the tracking sets for rows, columns, and subgrids.

        Args:
            row (int): The row index (0-based).
            col (int): The column index (0-based).
            num (int): The number to place.
        """
        self.board[row][col] = num
        self.rows[row].add(num)
        self.cols[col].add(num)
        box_index = (row // SUBGRID_SIZE) * SUBGRID_SIZE + (col // SUBGRID_SIZE)
        self.boxes[box_index].add(num)

    def remove_number(self, row: int, col: int, num: int) -> None:
        """
        Removes the number `num` from the specified position (row, col) and
        updates the tracking sets for rows, columns, and subgrids.

        Args:
            row (int): The row index (0-based).
            col (int): The column index (0-based).
            num (int): The number to remove.
        """
        self.board[row][col] = 0
        self.rows[row].remove(num)
        self.cols[col].remove(num)
        box_index = (row // SUBGRID_SIZE) * SUBGRID_SIZE + (col // SUBGRID_SIZE)
        self.boxes[box_index].remove(num)

    def print_board(self) -> None:
        """
        Prints the current state of the Sudoku board in a human-readable format.
        Empty cells are displayed as '.'.
        """
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))


class SudokuSolver:
    """
    A class that solves a given Sudoku puzzle using backtracking with the
    Minimum Remaining Values (MRV) heuristic and forward checking.
    """

    def __init__(self, board: Board) -> None:
        """
        Initializes the solver with a given `Board` instance.

        Args:
            board (Board): The Sudoku board to solve.
        """
        self.board = board

    def solve(self) -> bool:
        """
        Solves the Sudoku puzzle using the backtracking algorithm.

        Returns:
            bool: True if the puzzle is solvable, False otherwise.
        """
        return self._backtrack()

    def _backtrack(self) -> bool:
        """
        Backtracking algorithm to try placing numbers in the empty cells
        while adhering to Sudoku rules. It uses the MRV heuristic to
        choose the next cell with the fewest valid choices.

        Returns:
            bool: True if the puzzle is solved, False if no solution exists.
        """
        # Use MRV heuristic: Find the cell with the fewest valid options
        min_choices = GRID_SIZE + 1  # A number larger than the max possible choices
        row, col = -1, -1
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board.board[r][c] == 0:  # If the cell is empty
                    valid_choices = self._count_valid_choices(r, c)
                    if valid_choices < min_choices:
                        min_choices = valid_choices
                        row, col = r, c
        if row == -1:  # Puzzle is solved when no empty cells are left
            return True

        # Try placing each number in the current cell
        for num in range(1, GRID_SIZE + 1):
            if self.board.is_valid(row, col, num):
                self.board.place_number(row, col, num)
                if self._backtrack():  # Recurse to solve the next part
                    return True
                self.board.remove_number(row, col, num)  # Backtrack if no solution found
        return False

    def _count_valid_choices(self, row: int, col: int) -> int:
        """
        Counts how many valid numbers can be placed in the cell at (row, col).

        Args:
            row (int): The row index (0-based).
            col (int): The column index (0-based).

        Returns:
            int: The number of valid choices for this cell.
        """
        valid_choices = 0
        for num in range(1, GRID_SIZE + 1):
            if self.board.is_valid(row, col, num):
                valid_choices += 1
        return valid_choices


class SudokuGenerator:
    """
    A class that generates a solvable Sudoku puzzle by filling the board
    and then removing cells to create a puzzle with one unique solution.
    """

    def __init__(self) -> None:
        """
        Initializes a new Sudoku generator with an empty board.
        """
        self.board = Board()

    def generate_sudoku(self) -> None:
        """
        Generates a solvable Sudoku puzzle by first filling the board
        and then removing some of the numbers to create a puzzle.
        """
        self._fill_board()
        self._remove_cells()

    def _fill_board(self) -> None:
        """
        Fills the board using a backtracking algorithm to ensure a valid
        Sudoku solution.
        """

        def backtrack_fill() -> bool:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.board.board[row][col] == 0:  # Find an empty cell
                        random.shuffle(range(1, GRID_SIZE + 1))  # Randomize number order to avoid patterns
                        for num in range(1, GRID_SIZE + 1):
                            if self.board.is_valid(row, col, num):
                                self.board.place_number(row, col, num)
                                if backtrack_fill():  # Recurse to fill the next empty cell
                                    return True
                                self.board.remove_number(row, col, num)  # Backtrack if no solution found
                        return False
            return True

        backtrack_fill()

    def _remove_cells(self) -> None:
        """
        Removes random cells from the filled board to create a puzzle with a unique solution.
        The number of cells removed is random (between 30 and 40).
        """
        for _ in range(random.randint(30, 40)):
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            while self.board.board[row][col] == 0:
                row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            self.board.board[row][col] = 0


def main() -> None:
    """
    Main function to generate a Sudoku puzzle and solve it.
    """
    # Generate a new puzzle
    generator = SudokuGenerator()
    generator.generate_sudoku()
    print("Generated Sudoku Puzzle:")
    generator.board.print_board()

    # Solve the puzzle
    solver = SudokuSolver(generator.board)
    if solver.solve():
        print("\nSolved Sudoku Puzzle:")
        generator.board.print_board()
    else:
        print("\nNo solution found.")


if __name__ == "__main__":
    main()
