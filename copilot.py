import random


def create_board() -> list[list[int]]:
    """Generate a new Sudoku board"""
    board: list[list[int]] = [[0] * 9 for _ in range(9)]
    fill_diagonal_boxes(board)
    fill_remaining(board, 0, 3)
    return board


def fill_diagonal_boxes(board: list[list[int]]) -> None:
    """Fill the diagonal 3x3 boxes with random numbers"""
    for i in range(0, 9, 3):
        fill_box(board, i, i)


def fill_box(board: list[list[int]], row: int, col: int) -> None:
    """Fill a 3x3 box with random numbers"""
    num = random.sample(range(1, 10), 9)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = num.pop()


def is_safe(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if it's safe to place a number in the position"""
    return (
        not used_in_row(board, row, num)
        and not used_in_col(board, col, num)
        and not used_in_box(board, row - row % 3, col - col % 3, num)
    )


def used_in_row(board: list[list[int]], row: int, num: int) -> bool:
    """Check if a number is used in the row"""
    return num in board[row]


def used_in_col(board: list[list[int]], col: int, num: int) -> bool:
    """Check if a number is used in the column"""
    return num in [board[row][col] for row in range(9)]


def used_in_box(
    board: list[list[int]], box_start_row: int, box_start_col: int, num: int
) -> bool:
    """Check if a number is used in the 3x3 box"""
    for i in range(3):
        for j in range(3):
            if board[i + box_start_row][j + box_start_col] == num:
                return True
    return False


def fill_remaining(board: list[list[int]], i: int, j: int) -> bool:
    """Recursively fill the remaining cells"""
    if j >= 9 and i < 8:
        i, j = i + 1, 0
    if i >= 9 and j >= 9:
        return True
    if i < 3:
        if j < 3:
            j = 3
    elif i < 6:
        if j == int(i / 3) * 3:
            j += 3
    else:
        if j == 6:
            i, j = i + 1, 0
            if i >= 9:
                return True
    for num in range(1, 10):
        if is_safe(board, i, j, num):
            board[i][j] = num
            if fill_remaining(board, i, j + 1):
                return True
            board[i][j] = 0
    return False


def remove_numbers(board: list[list[int]], num_holes: int) -> None:
    """Remove numbers from the board to create a puzzle"""
    while num_holes > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            num_holes -= 1


def print_board(board: list[list[int]]) -> None:
    """Print the Sudoku board"""
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))


if __name__ == "__main__":
    board = create_board()
    remove_numbers(board, 40)  # Remove 40 numbers to create the puzzle
    print_board(board)
