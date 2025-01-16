import random
from typing import List, Optional

N = 9  # Board size


def print_board(board: List[List[int]]) -> None:
    """Prints the Sudoku board with enhanced formatting."""
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(str(board[i][j]) if board[i][j] != 0 else ".", end=" ")
        print()


def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    """Checks if placing num at (row, col) is valid."""
    # Use sets for faster lookups
    row_set = set(board[row])
    col_set = {board[i][col] for i in range(N)}
    subgrid_set = {
        board[i + row // 3 * 3][j + col // 3 * 3] for i in range(3) for j in range(3)
    }
    return num not in row_set and num not in col_set and num not in subgrid_set


def solve(board: List[List[int]]) -> bool:
    """Solves the Sudoku puzzle using backtracking."""
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False
    return True


def generate_sudoku(difficulty: int = 40) -> Optional[List[List[int]]]:
    """Generates a Sudoku puzzle with a specified difficulty (number of empty cells)."""
    board: List[List[int]] = [[0] * N for _ in range(N)]

    # Fill diagonal blocks for a faster, valid starting point
    for i in range(0, N, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for r in range(3):
            for c in range(3):
                board[i + r][i + c] = nums.pop()

    if not solve(board):
        return None

    # Remove numbers to create the puzzle.  More efficient removal strategy
    empty_cells = 81 - difficulty
    removed_cells = 0
    while removed_cells < empty_cells:
        row, col = random.randint(0, N - 1), random.randint(0, N - 1)
        if board[row][col] != 0:
            board[row][col] = 0
            removed_cells += 1

    return board


if __name__ == "__main__":
    board = generate_sudoku()
    if board:
        print_board(board)
    else:
        print("Could not generate a valid Sudoku puzzle.")
