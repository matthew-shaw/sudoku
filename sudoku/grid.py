class Grid:
    """A Sudoku puzzle grid of nxn dimensions."""

    def __init__(self, rows: int = 9, columns: int = 9) -> None:
        """Create a new emptpy Sudoku grid."""
        self._rows: int = rows
        self._columns: int = columns
        self._content: list[list[int]] = []

        # Initialise the grid with zeros
        for _x in range(self._rows):
            row: list[int] = []
            for _y in range(self._columns):
                row.append(0)
            self._content.append(row)
