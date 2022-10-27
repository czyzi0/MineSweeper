#pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

import itertools
import random
from collections import defaultdict, namedtuple
from typing import DefaultDict, Set, Tuple


MinesweeperParams = namedtuple('MinesweeperParams', ['n_cols', 'n_rows', 'n_mines'])


class MinesweeperModel:

    def __init__(self, params: MinesweeperParams):
        self._params: MinesweeperParams = params

        self._mines: Set[Tuple[int, int]]
        self._numbers: DefaultDict[Tuple[int, int], int]

        self._revealed: Set[Tuple[int, int]]
        self._flags: Set[Tuple[int, int]]

        self.reset()

    def reset(self) -> None:
        # Set mines
        self._mines = set()
        while len(self._mines) < self.n_mines:
            self._mines.add((
                random.randint(0, self.n_cols - 1),
                random.randint(0, self.n_rows - 1)
            ))
        # Calculate numbers
        self._numbers = defaultdict(int)
        for col, row in self._mines:
            for col_, row_ in self._neighbors(col, row):
                if not self.is_mine(col_, row_):
                    self._numbers[(col_, row_)] += 1
        # Others
        self._revealed = set()
        self._flags = set()

    @property
    def lost(self) -> bool:
        return bool(self._mines.intersection(self._revealed))

    @property
    def won(self) -> bool:
        return (
            len(self._mines.union(self._revealed)) == self._params.n_cols * self._params.n_rows)

    @property
    def n_cols(self) -> int:
        return self._params.n_cols

    @property
    def n_rows(self) -> int:
        return self._params.n_rows

    @property
    def n_mines(self) -> int:
        return self._params.n_mines

    @property
    def n_flags(self) -> int:
        return len(self._flags)

    def is_mine(self, col: int, row: int) -> bool:
        return (col, row) in self._mines

    def is_flag(self, col: int, row: int) -> bool:
        return (col, row) in self._flags

    def is_revealed(self, col: int, row: int) -> bool:
        return (col, row) in self._revealed

    def get_number(self, col: int, row: int) -> int:
        return self._numbers[(col, row)]

    def is_in_board(self, col: int, row: int) -> bool:
        return 0 <= col < self.n_cols and 0 <= row < self.n_rows

    def toggle_flag(self, col: int, row: int) -> None:
        if self.is_revealed(col, row):
            return

        if (col, row) in self._flags:
            self._flags.remove((col, row))
        else:
            self._flags.add((col, row))

    def reveal(self, col: int, row: int) -> None:
        if self.is_flag(col, row):
            return
        self._reveal(col, row)

    def _reveal(self, col: int, row: int) -> None:
        if self.is_revealed(col, row):
            return

        self._revealed.add((col, row))

        if self.is_flag(col, row):
            self._flags.remove((col, row))

        if self.is_mine(col, row):
            self._revealed.update(self._mines)

        if not self.is_mine(col, row) and self.get_number(col, row) == 0:
            for col_, row_ in self._neighbors(col, row):
                self._reveal(col_, row_)

    def _neighbors(self, col: int, row: int):
        for dcol, drow in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if dcol == 0 and drow == 0:
                continue
            col_ = col + dcol
            row_ = row + drow
            if not self.is_in_board(col_, row_):
                continue
            yield col_, row_
