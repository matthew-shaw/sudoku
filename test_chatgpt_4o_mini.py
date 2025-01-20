import pytest

from .chatgpt_4o_mini import GRID_SIZE, Board, SudokuGenerator, SudokuSolver


# Test Board initialization
def test_board_initialization():
    board = Board()
    # Ensure all cells are initialized to 0
    assert all(board.board[r][c] == 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE))


# Test valid number placement and removal
def test_place_and_remove_number():
    board = Board()

    # Place a valid number
    board.place_number(0, 0, 5)
    assert board.board[0][0] == 5  # Check if the number is placed correctly
    assert 5 in board.rows[0]  # Number should be in the row set
    assert 5 in board.cols[0]  # Number should be in the column set
    assert 5 in board.boxes[0]  # Number should be in the subgrid set

    # Remove the number
    board.remove_number(0, 0, 5)
    assert board.board[0][0] == 0  # The cell should be reset to 0
    assert 5 not in board.rows[0]  # Number should be removed from the row set
    assert 5 not in board.cols[0]  # Number should be removed from the column set
    assert 5 not in board.boxes[0]  # Number should be removed from the subgrid set


# Test if a number is valid in a specific position
def test_is_valid():
    board = Board()

    # Place some numbers
    board.place_number(0, 0, 5)
    board.place_number(1, 1, 3)

    # Valid move for 5 in an empty cell
    assert board.is_valid(2, 2, 5) is True  # 5 is not in row 2, column 2, or the box

    # Invalid move for 5 in row 0 (already placed)
    assert board.is_valid(0, 1, 5) is False  # 5 is in row 0

    # Invalid move for 3 in column 1 (already placed)
    assert board.is_valid(2, 1, 3) is False  # 3 is in column 1


# Test solving a puzzle
def test_sudoku_solver():
    # A simple solvable puzzle
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board()
    board.board = puzzle  # Load the puzzle into the board
    solver = SudokuSolver(board)

    # Solve the puzzle
    solved = solver.solve()

    # Ensure the puzzle is solved correctly
    assert solved is True
    assert board.board[0][2] == 4  # Check if a known position is correctly solved
    assert board.board[8][8] == 9  # Another known solved position


# Test puzzle generation and validity
def test_sudoku_generator():
    generator = SudokuGenerator()
    generator.generate_sudoku()

    # Ensure the generated puzzle has empty cells
    empty_cells = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if generator.board.board[r][c] == 0)
    assert empty_cells >= 30  # The puzzle should have at least 30 empty cells

    # Check that the generated board is solvable
    solver = SudokuSolver(generator.board)
    solved = solver.solve()
    assert solved is True  # The generated puzzle should be solvable


# Test invalid Sudoku puzzle that can't be solved
def test_unsolvable_puzzle():
    unsolvable_puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # Alter the puzzle to make it unsolvable (e.g., adding a contradiction)
    unsolvable_puzzle[0][0] = 6  # This creates a conflict in the first row

    board = Board()
    board.board = unsolvable_puzzle  # Load the unsolvable puzzle into the board
    solver = SudokuSolver(board)

    # Try to solve the puzzle
    solved = solver.solve()

    # Ensure the puzzle cannot be solved
    assert solved is False


if __name__ == "__main__":
    pytest.main()
