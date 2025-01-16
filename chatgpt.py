import random
from typing import List, Optional

N = 9  # Board size


def print_board(board: List[List[int]]) -> None:
    """Prints the Sudoku board with enhanced formatting, including separators for 3x3 blocks.

    Args:
        board: A 9x9 list of lists representing the Sudoku board. 0 represents an empty cell.
    """
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Separator line between 3x3 blocks
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # Separator between 3x3 blocks
            print(str(board[i][j]) if board[i][j] != 0 else ".", end=" ")  # Print cell value or '.'
        print()


def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    """Checks if placing 'num' at (row, col) is valid using sets for efficiency.

    Args:
        board: The Sudoku board.
        row: The row index (0-8).
        col: The column index (0-8).
        num: The number to check (1-9).

    Returns:
        True if placing 'num' at (row, col) is valid, False otherwise.
    """
    row_set: set[int] = set(board[row])  # Create a set of numbers in the row
    col_set: set[int] = {board[i][col] for i in range(N)}  # Create a set of numbers in the column
    subgrid_row: int = (row // 3) * 3  # Calculate subgrid starting row
    subgrid_col: int = (col // 3) * 3  # Calculate subgrid starting column
    subgrid_set: set[int] = {
        board[subgrid_row + i][subgrid_col + j] for i in range(3) for j in range(3)
    }  # Create a set of numbers in the 3x3 subgrid
    return num not in row_set and num not in col_set and num not in subgrid_set


def solve(board: List[List[int]]) -> bool:
    """Solves the Sudoku puzzle using backtracking.

    Args:
        board: The Sudoku board (modified in place if a solution is found).

    Returns:
        True if a solution is found, False otherwise.
    """
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:  # Find an empty cell
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):  # Recursive call to solve the rest
                            return True
                        board[row][col] = 0  # Backtrack if the current number doesn't lead to a solution
                return False  # No valid number found for this cell
    return True  # Puzzle solved


def generate_sudoku(difficulty: int = 40) -> Optional[List[List[int]]]:
    """Generates a Sudoku puzzle of the specified difficulty (number of empty cells).

    Args:
        difficulty: The desired number of empty cells (default is 40). Higher values mean easier puzzles.

    Returns:
        A list of lists representing the Sudoku puzzle, or None if a puzzle cannot be generated
        at the specified difficulty.
    """
    board: List[List[int]] = [[0] * N for _ in range(N)]  # Initialize an empty 9x9 board

    # Fill diagonal blocks for a faster, valid starting point
    for i in range(0, N, 3):
        nums: list[int] = list(range(1, 10))  # List of numbers 1-9
        random.shuffle(nums)  # Shuffle the numbers randomly
        for r in range(3):
            for c in range(3):
                board[i + r][i + c] = nums.pop()  # Fill the diagonal blocks

    if not solve(board):  # Check if a solution exists after pre-filling
        return None  # Could not generate a puzzle

    # Remove numbers to create the puzzle. More efficient removal.
    empty_cells: int = 81 - difficulty  # Number of empty cells to create
    removed_cells: int = 0  # Counter for the number of cells removed
    while removed_cells < empty_cells:
        row: int = random.randint(0, N - 1)  # Randomly select a row
        col: int = random.randint(0, N - 1)  # Randomly select a column
        if board[row][col] != 0:  # Check if the cell is not already empty
            board[row][col] = 0  # Empty the cell
            removed_cells += 1  # Increment the counter

    return board


if __name__ == "__main__":
    board = generate_sudoku()
    if board:
        print_board(board)
    else:
        print("Could not generate a valid Sudoku puzzle.")
