import random
from typing import List


class SudokuGenerator:
    def __init__(self, missing_digits: int) -> None:
        """Initialize the generator with number of cells to remove"""
        self.missing_digits: int = missing_digits
        self.box_size: int = 3  # Size of 3x3 boxes
        self.grid_size: int = self.box_size * self.box_size  # 9x9 grid
        self.grid: List[List[int]] = [
            [0 for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """Check if a number can be placed in a given cell"""
        # Check row
        if num in self.grid[row]:
            return False

        # Check column
        if num in [self.grid[i][col] for i in range(self.grid_size)]:
            return False

        # Check 3x3 box
        box_row: int = row - row % self.box_size
        box_col: int = col - col % self.box_size
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if self.grid[i][j] == num:
                    return False
        return True

    def solve_grid(self, row: int = 0, col: int = 0) -> bool:
        """Solve the Sudoku grid using backtracking"""
        if col == self.grid_size:
            row += 1
            col = 0
        if row == self.grid_size:
            return True

        if self.grid[row][col] != 0:
            return self.solve_grid(row, col + 1)

        for num in range(1, self.grid_size + 1):
            if self.is_valid_move(row, col, num):
                self.grid[row][col] = num
                if self.solve_grid(row, col + 1):
                    return True
                self.grid[row][col] = 0
        return False

    def generate_puzzle(self) -> None:
        """Generate a complete Sudoku puzzle"""
        # Fill diagonal boxes first (they are independent of each other)
        for i in range(0, self.grid_size, self.box_size):
            self._fill_box(i, i)

        # Fill remaining cells
        self.solve_grid()

        # Remove digits to create puzzle
        self._remove_digits()

    def _fill_box(self, row: int, col: int) -> None:
        """Fill a 3x3 box with random numbers"""
        numbers: List[int] = list(range(1, self.grid_size + 1))
        random.shuffle(numbers)

        for i in range(self.box_size):
            for j in range(self.box_size):
                self.grid[row + i][col + j] = numbers.pop()

    def _remove_digits(self) -> None:
        """Remove random digits to create the puzzle"""
        count: int = self.missing_digits
        while count > 0:
            row: int = random.randint(0, self.grid_size - 1)
            col: int = random.randint(0, self.grid_size - 1)

            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                count -= 1

    def print_grid(self) -> None:
        """Print the Sudoku grid in a readable format"""
        for i in range(self.grid_size):
            if i % self.box_size == 0 and i != 0:
                print("-" * (self.grid_size * 2 + self.box_size + 1))

            for j in range(self.grid_size):
                if j % self.box_size == 0 and j != 0:
                    print("|", end=" ")

                if j == self.grid_size - 1:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")


def main() -> None:
    # Create a puzzle with 30 missing digits (adjust this number for different difficulty levels)
    puzzle: SudokuGenerator = SudokuGenerator(30)
    print("Generating new Sudoku puzzle...")
    puzzle.generate_puzzle()
    print("\nYour Sudoku Puzzle (0 represents empty cells):")
    puzzle.print_grid()


if __name__ == "__main__":
    main()
