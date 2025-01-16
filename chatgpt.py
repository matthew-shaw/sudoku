import random

# Define the size of the board (9x9)
N = 9


def print_board(board: list[list[int]]) -> None:
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))


def is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    # Check if the number exists in the row
    for c in range(N):
        if board[row][c] == num:
            return False

    # Check if the number exists in the column
    for r in range(N):
        if board[r][col] == num:
            return False

    # Check if the number exists in the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True


def solve(board: list[list[int]]) -> bool:
    # Try to find the next empty cell
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                for num in range(1, N + 1):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_sudoku() -> list[list[int]]:
    board: list[list[int]] = [[0] * N for _ in range(N)]

    # Try to fill the board with a valid solution
    solve(board)

    # Remove random numbers to create the puzzle
    difficulty = random.choice([40, 45, 50, 55])  # Number of empty cells to remove
    attempts = difficulty

    while attempts > 0:
        row, col = random.randint(0, N - 1), random.randint(0, N - 1)
        if board[row][col] != 0:
            board[row][col] = 0
            attempts -= 1

    return board


# Generate a Sudoku puzzle and print it
puzzle = generate_sudoku()
print_board(puzzle)
