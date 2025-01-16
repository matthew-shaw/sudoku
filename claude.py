import random
from typing import List

N = 9  # Board size


class SudokuGenerator:
    """Generates and solves Sudoku puzzles."""

    def __init__(self, difficulty: int = 40) -> None:
        """Initializes the Sudoku generator with a specified difficulty level.

        Args:
            difficulty: The desired number of empty cells in the generated puzzle (default is 40).  Higher numbers mean easier puzzles.
        """
        self.difficulty: int = difficulty
        self.board: List[List[int]] = [[0] * N for _ in range(N)]  # Initialize empty 9x9 board
        try:
            self.generate_puzzle()
        except ValueError as e:
            print(f"Error generating puzzle: {e}")
            self.board = [[0] * N for _ in range(N)]  # Create an empty board if generation fails

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Checks if placing 'num' at (row, col) is valid.

        Args:
            row: The row index (0-8).
            col: The column index (0-8).
            num: The number to place (1-9).

        Returns:
            True if the placement is valid, False otherwise.
        """
        return (
            num not in self.board[row]
            and num not in [self.board[i][col] for i in range(N)]
            and num not in [self.board[i + row // 3 * 3][j + col // 3 * 3] for i in range(3) for j in range(3)]
        )

    def solve(self, row: int = 0, col: int = 0) -> bool:
        """Recursively solves the Sudoku puzzle using backtracking.

        Args:
            row: The current row (starts at 0).
            col: The current column (starts at 0).

        Returns:
            True if a solution is found, False otherwise.
        """
        if col == N:
            row += 1
            col = 0
        if row == N:
            return True  # Puzzle is solved

        if self.board[row][col] != 0:
            return self.solve(row, col + 1)  # Cell is already filled

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve(row, col + 1):
                    return True  # Solution found
                self.board[row][col] = 0  # Backtrack: remove number if it doesn't lead to a solution
        return False  # No valid number found for this cell

    def generate_puzzle(self) -> None:
        """Generates a Sudoku puzzle with the specified difficulty.

        Fills the diagonal 3x3 blocks, solves the puzzle, then removes cells to reach the desired difficulty.
        Raises ValueError if a solvable puzzle cannot be created.
        """
        # Fill diagonal blocks for faster solving and a valid starting point.
        for i in range(0, N, 3):
            nums: list[int] = list(range(1, 10))  # added type hint
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    self.board[i + r][i + c] = nums.pop()

        if not self.solve():  # Check if a solution exists after pre-filling
            raise ValueError("Could not create a solvable Sudoku puzzle.")

        # Remove numbers to create the puzzle
        empty_cells: int = 81 - self.difficulty  # added type hint
        cells_to_remove: int = 0  # added type hint
        while cells_to_remove < empty_cells:
            row: int = random.randint(0, 8)  # added type hint
            col: int = random.randint(0, 8)  # added type hint
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
