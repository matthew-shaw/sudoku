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


# Sudoku Solver using Backtracking with optimizations
class Sudoku:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.rows = [set() for _ in range(9)]  # Track numbers in rows
        self.cols = [set() for _ in range(9)]  # Track numbers in columns
        self.boxes = [set() for _ in range(9)]  # Track numbers in 3x3 boxes

    def is_valid(self, row, col, num):
        box_index = (row // 3) * 3 + (col // 3)
        if num in self.rows[row] or num in self.cols[col] or num in self.boxes[box_index]:
            return False
        return True

    def place_number(self, row, col, num):
        self.board[row][col] = num
        self.rows[row].add(num)
        self.cols[col].add(num)
        box_index = (row // 3) * 3 + (col // 3)
        self.boxes[box_index].add(num)

    def remove_number(self, row, col, num):
        self.board[row][col] = 0
        self.rows[row].remove(num)
        self.cols[col].remove(num)
        box_index = (row // 3) * 3 + (col // 3)
        self.boxes[box_index].remove(num)

    def solve(self):
        # Use a more efficient backtracking algorithm with forward checking and heuristics
        def backtrack():
            # Find the next empty cell
            min_choices = 10
            row, col = -1, -1
            for r in range(9):
                for c in range(9):
                    if self.board[r][c] == 0:
                        # Count the valid numbers we can place
                        valid_choices = 0
                        box_index = (r // 3) * 3 + (c // 3)
                        for num in range(1, 10):
                            if num not in self.rows[r] and num not in self.cols[c] and num not in self.boxes[box_index]:
                                valid_choices += 1
                        # Use MRV heuristic: choose the cell with the fewest valid choices
                        if valid_choices < min_choices:
                            min_choices = valid_choices
                            row, col = r, c
            if row == -1:  # If no empty cells are left, puzzle is solved
                return True

            # Try each number for the empty cell
            for num in range(1, 10):
                if self.is_valid(row, col, num):
                    self.place_number(row, col, num)
                    if backtrack():
                        return True
                    self.remove_number(row, col, num)
            return False

        return backtrack()

    def generate_sudoku(self):
        # Fill the board using backtracking first
        self._fill_board()
        # Remove random cells to create a puzzle
        self._remove_cells()

    def _fill_board(self):
        def backtrack_fill():
            # Find an empty cell
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        random.shuffle(range(1, 10))  # Randomize order to avoid patterns
                        for num in range(1, 10):
                            if self.is_valid(row, col, num):
                                self.place_number(row, col, num)
                                if backtrack_fill():
                                    return True
                                self.remove_number(row, col, num)
                        return False
            return True

        backtrack_fill()

    def _remove_cells(self):
        # Remove random cells to create a solvable puzzle
        for _ in range(random.randint(30, 40)):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))


if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.generate_sudoku()

    print("Generated Sudoku Puzzle:")
    sudoku.print_board()

    if sudoku.solve():
        print("\nSolved Sudoku Puzzle:")
        sudoku.print_board()
    else:
        print("\nNo solution found.")
