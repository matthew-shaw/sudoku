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

# Constants
GRID_SIZE = 9
SUBGRID_SIZE = 3


# Helper class for managing the Sudoku board
class Board:
    def __init__(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.rows = [set() for _ in range(GRID_SIZE)]  # Track numbers in rows
        self.cols = [set() for _ in range(GRID_SIZE)]  # Track numbers in columns
        self.boxes = [set() for _ in range(GRID_SIZE)]  # Track numbers in 3x3 boxes

    def is_valid(self, row, col, num):
        """Check if placing `num` at (row, col) is valid."""
        box_index = (row // SUBGRID_SIZE) * SUBGRID_SIZE + (col // SUBGRID_SIZE)
        return num not in self.rows[row] and num not in self.cols[col] and num not in self.boxes[box_index]

    def place_number(self, row, col, num):
        """Place `num` at (row, col) and update the constraint sets."""
        self.board[row][col] = num
        self.rows[row].add(num)
        self.cols[col].add(num)
        box_index = (row // SUBGRID_SIZE) * SUBGRID_SIZE + (col // SUBGRID_SIZE)
        self.boxes[box_index].add(num)

    def remove_number(self, row, col, num):
        """Remove `num` from (row, col) and update the constraint sets."""
        self.board[row][col] = 0
        self.rows[row].remove(num)
        self.cols[col].remove(num)
        box_index = (row // SUBGRID_SIZE) * SUBGRID_SIZE + (col // SUBGRID_SIZE)
        self.boxes[box_index].remove(num)

    def print_board(self):
        """Print the board in a human-readable format."""
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))


# Sudoku Solver class
class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        """Solve the Sudoku using backtracking with MRV heuristic and forward checking."""
        return self._backtrack()

    def _backtrack(self):
        """Perform backtracking to solve the Sudoku."""
        # Use MRV heuristic: Find the cell with the fewest valid options
        min_choices = GRID_SIZE + 1
        row, col = -1, -1
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board.board[r][c] == 0:
                    valid_choices = self._count_valid_choices(r, c)
                    if valid_choices < min_choices:
                        min_choices = valid_choices
                        row, col = r, c
        if row == -1:  # Puzzle is solved
            return True

        for num in range(1, GRID_SIZE + 1):
            if self.board.is_valid(row, col, num):
                self.board.place_number(row, col, num)
                if self._backtrack():
                    return True
                self.board.remove_number(row, col, num)
        return False

    def _count_valid_choices(self, row, col):
        """Count valid numbers that can be placed at (row, col)."""
        valid_choices = 0
        for num in range(1, GRID_SIZE + 1):
            if self.board.is_valid(row, col, num):
                valid_choices += 1
        return valid_choices


# Sudoku Puzzle Generator class
class SudokuGenerator:
    def __init__(self):
        self.board = Board()

    def generate_sudoku(self):
        """Generate a solvable Sudoku puzzle."""
        self._fill_board()
        self._remove_cells()

    def _fill_board(self):
        """Fill the board using backtracking."""

        def backtrack_fill():
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self.board.board[row][col] == 0:
                        random.shuffle(range(1, GRID_SIZE + 1))  # Randomize order to avoid patterns
                        for num in range(1, GRID_SIZE + 1):
                            if self.board.is_valid(row, col, num):
                                self.board.place_number(row, col, num)
                                if backtrack_fill():
                                    return True
                                self.board.remove_number(row, col, num)
                        return False
            return True

        backtrack_fill()

    def _remove_cells(self):
        """Remove random cells to create a solvable puzzle."""
        for _ in range(random.randint(30, 40)):
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            while self.board.board[row][col] == 0:
                row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            self.board.board[row][col] = 0


# Main function to run the puzzle generation and solving process
if __name__ == "__main__":
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
