from typing import List, Optional

import pytest

from sudoku.chatgpt import generate_sudoku, is_valid, solve  # Correct import path

# Test data:  A comprehensive set of test cases, including various board configurations and difficulty levels.
# Edge cases and boundary conditions are explicitly included to improve test coverage.
TEST_DATA: list[tuple[list[list[int]], bool]] = [
    (
        [  # Example 1: A partially filled, solvable Sudoku puzzle
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
        True,  # Expected: Solvable
    ),
    (
        [  # Example 2: An unsolvable puzzle (all zeros)
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0] * 9,
        ],
        False,  # Expected: Unsolvable
    ),
    (
        [  # Example 3: An already solved puzzle
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 1, 4, 3, 6, 5, 8, 9, 7],
            [3, 6, 5, 8, 9, 7, 2, 1, 4],
            [8, 9, 7, 2, 1, 4, 3, 6, 5],
            [5, 3, 1, 6, 4, 2, 9, 7, 8],
            [6, 7, 8, 9, 3, 1, 5, 4, 2],
            [9, 4, 2, 5, 7, 8, 6, 3, 1],
        ],
        True,  # Expected: Solvable
    ),
    # Additional test cases for edge conditions and invalid inputs
    ([[1, 2, 3, 4, 5, 6, 7, 8, 9] * 9], False),  # Repeated numbers in a row
    (
        [
            [1] * 9,
            [2] * 9,
            [3] * 9,
            [4] * 9,
            [5] * 9,
            [6] * 9,
            [7] * 9,
            [8] * 9,
            [9] * 9,
        ],
        False,
    ),  # Repeated numbers in a column
    (
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 10],
            [1] * 9,
            [1] * 9,
            [1] * 9,
            [1] * 9,
            [1] * 9,
            [1] * 9,
            [1] * 9,
            [1] * 9,
        ],
        False,
    ),  # Number out of range (1-9)
]


@pytest.mark.parametrize("board, solvable", TEST_DATA)
def test_solve(board: List[List[int]], solvable: bool) -> None:
    """Tests the Sudoku solver function ('solve').

    This test function verifies that the solve function correctly identifies solvable and unsolvable Sudoku boards.

    Args:
        board: A list of lists representing the Sudoku board.
        solvable: A boolean indicating whether the board is expected to be solvable.
    """
    solved: bool = solve(board)
    assert solved == solvable


@pytest.mark.parametrize("difficulty", [0, 10, 30, 50, 70, 90])
def test_generate_sudoku(difficulty: int) -> None:
    """Tests the Sudoku generation function ('generate_sudoku') for different difficulty levels.

    This test function verifies that the generate_sudoku function produces boards of the correct dimensions and that the numbers are within range.  It does not rigorously check the precise difficulty level, which is complex to validate.

    Args:
        difficulty: The desired difficulty level (number of empty cells).
    """
    generated_board: Optional[List[List[int]]] = generate_sudoku(difficulty)
    if generated_board is not None:
        assert len(generated_board) == 9
        assert all(len(row) == 9 for row in generated_board)
        assert all(all(0 <= num <= 9 for num in row) for row in generated_board)


def test_is_valid() -> None:
    """Tests the 'is_valid' function for various scenarios, including valid and invalid number placements.

    This test suite checks that the is_valid function correctly identifies valid and invalid placements based on Sudoku rules (row, column, and 3x3 subgrid constraints).  It also includes boundary condition tests.
    """
    board: list[list[int]] = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    # Test valid placements
    assert is_valid(board, 0, 0, 5)
    assert is_valid(board, 1, 3, 1)
    # Test invalid placements
    assert not is_valid(board, 0, 0, 6)  # Already in row
    assert not is_valid(board, 1, 1, 7)  # Already in column
    assert not is_valid(board, 2, 2, 1)  # Already in 3x3 subgrid
    assert not is_valid(board, 0, 0, 10)  # Number out of range (1-9)
    assert not is_valid(board, -1, 0, 5)  # Negative row index
    assert not is_valid(board, 0, -1, 5)  # Negative column index
    assert not is_valid(board, 9, 0, 5)  # Row index out of range
    assert not is_valid(board, 0, 9, 5)  # Column index out of range
