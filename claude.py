import random
from typing import List

N = 9  # Board size


class SudokuGenerator:
    def __init__(self, difficulty: int = 40) -> None:
        """Initializes the Sudoku generator with a specified difficulty (number of empty cells)."""
        self.difficulty: int = difficulty
        self.board: List[List[int]] = [[0] * N for _ in range(N)]
        self.generate_puzzle()

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Checks if placing 'num' at (row, col) is valid."""
        return (
            num not in self.board[row]
            and num not in [self.board[i][col] for i in range(N)]
            and num
            not in [
                self.board[i + row // 3 * 3][j + col // 3 * 3]
                for i in range(3)
                for j in range(3)
            ]
        )

    def solve(self, row: int = 0, col: int = 0) -> bool:
        """Solves the Sudoku puzzle using backtracking."""
        if col == N:
            row += 1
            col = 0
        if row == N:
            return True

        if self.board[row][col] != 0:
            return self.solve(row, col + 1)

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve(row, col + 1):
                    return True
                self.board[row][col] = 0  # Backtrack
        return False

    def generate_puzzle(self) -> None:
        """Generates a Sudoku puzzle."""
        # Fill diagonal blocks for faster solving and a valid starting point.
        for i in range(0, N, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    self.board[i + r][i + c] = nums.pop()

        if not self.solve():  # Check if a solution exists after pre-filling
            raise ValueError("Could not create a solvable Sudoku puzzle.")

        # More efficient removal strategy:  Remove cells one at a time until difficulty is met.
        empty_cells = 81 - self.difficulty
        cells_to_remove = 0
        while cells_to_remove < empty_cells:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove += 1

    def print_board(self) -> None:
        """Prints the Sudoku board with formatting."""
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
