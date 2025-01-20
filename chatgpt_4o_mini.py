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


# Sudoku Solver using Backtracking
def is_valid(board, row, col, num):
    # Check if the number is not repeated in the row, column, or 3x3 box
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


# Sudoku Puzzle Generator
def generate_sudoku():
    # Create an empty 9x9 board
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill diagonal 3x3 boxes
    for i in range(0, 9, 3):
        num_list = list(range(1, 10))
        random.shuffle(num_list)
        index = 0
        for row in range(i, i + 3):
            for col in range(i, i + 3):
                board[row][col] = num_list[index]
                index += 1

    # Solve the puzzle to fill remaining cells
    solve_sudoku(board)

    # Remove some numbers to create a puzzle
    for _ in range(random.randint(30, 40)):  # Randomly remove 30-40 elements
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return board


# Print the board in a readable format
def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))


# Generate and solve the Sudoku puzzle
if __name__ == "__main__":
    puzzle = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_board(puzzle)

    if solve_sudoku(puzzle):
        print("\nSolved Sudoku Puzzle:")
        print_board(puzzle)
    else:
        print("\nNo solution found.")
