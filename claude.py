import random
from typing import List

N = 9  # Size of the Sudoku board (9x9)


class SudokuGenerator:
    """Generates and solves Sudoku puzzles.

    This class provides methods to generate Sudoku puzzles of a specified difficulty,
    solve Sudoku puzzles, and print the board in a user-friendly format.
    """

    def __init__(self, difficulty: int = 40) -> None:
        """Initializes the Sudoku generator with a specified difficulty level.

        Args:
            difficulty: The desired number of empty cells in the generated puzzle (default is 40).
                        Higher values result in easier puzzles.
        """
        self.difficulty: int = difficulty
        self.board: List[List[int]] = [[0] * N for _ in range(N)]  # Initialize an empty 9x9 board
        try:
            self.generate_puzzle()
        except ValueError as e:
            print(f"Error generating puzzle: {e}")
            self.board = [[0] * N for _ in range(N)]  # Create an empty board if generation fails

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Checks if placing 'num' at (row, col) is valid according to Sudoku rules.

        Args:
            row: The row index (0-8).
            col: The column index (0-8).
            num: The number to place (1-9).

        Returns:
            True if the placement is valid, False otherwise.
        """
        row_set: set[int] = set(self.board[row])  # Numbers present in the current row
        col_set: set[int] = {self.board[i][col] for i in range(N)}  # Numbers present in the current column
        subgrid_row: int = (row // 3) * 3  # Starting row index of the 3x3 subgrid
        subgrid_col: int = (col // 3) * 3  # Starting column index of the 3x3 subgrid
        subgrid_set: set[int] = {
            self.board[subgrid_row + i][subgrid_col + j] for i in range(3) for j in range(3)
        }  # Numbers present in the 3x3 subgrid

        return num not in row_set and num not in col_set and num not in subgrid_set

    def solve(self, row: int = 0, col: int = 0) -> bool:
        """Recursively solves the Sudoku puzzle using backtracking.

        Args:
            row: The current row index (default is 0).
            col: The current column index (default is 0).

        Returns:
            True if a solution is found, False otherwise.
        """
        if col == N:  # Move to the next row if the current row is complete
            row += 1
            col = 0
        if row == N:
            return True  # Puzzle is solved

        if self.board[row][col] != 0:  # Cell is already filled, move to the next cell
            return self.solve(row, col + 1)

        for num in range(1, 10):  # Try numbers 1-9
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve(row, col + 1):  # Recursively try to solve the rest of the puzzle
                    return True
                self.board[row][col] = 0  # Backtrack if the current number doesn't lead to a solution
        return False  # No valid number found for this cell

    def generate_puzzle(self) -> None:
        """Generates a Sudoku puzzle with the specified difficulty.

        This method first fills the diagonal 3x3 blocks with random numbers, then solves the puzzle
        to ensure a valid solution exists. Finally, it removes cells to reach the desired difficulty level.
        Raises a ValueError if a solvable puzzle cannot be created.
        """
        # Fill diagonal blocks for faster solving and a valid starting point.  These blocks are independent.
        for i in range(0, N, 3):
            nums: list[int] = list(range(1, 10))
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    self.board[i + r][i + c] = nums.pop()

        if not self.solve():  # Check if a solution exists after pre-filling
            raise ValueError("Could not create a solvable Sudoku puzzle.")

        # Remove numbers to create the puzzle. Efficiently removes only filled cells.
        empty_cells: int = 81 - self.difficulty
        cells_to_remove: int = 0
        while cells_to_remove < empty_cells:
            row: int = random.randint(0, 8)
            col: int = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove += 1

    def print_board(self) -> None:
        """Prints the Sudoku board with formatting, including separators for 3x3 blocks."""
        for i in range(N):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(N):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(str(self.board[i][j]) if self.board[i][j] != 0 else ".", end=" ")
            print()


if __name__ == "__main__":
    sudoku = SudokuGenerator()
    sudoku.print_board()
