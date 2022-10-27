import itertools
import random
from collections import defaultdict, namedtuple
from typing import DefaultDict, Set, Tuple


MinesweeperParams = namedtuple('MinesweeperParams', ['n_cols', 'n_rows', 'n_mines'])


class MinesweeperModel:

    def __init__(self, params: MinesweeperParams):
        self.params: MinesweeperParams = params

        self.mines: Set[Tuple[int, int]] = set()
        self.numbers: DefaultDict[Tuple[int, int], int] = defaultdict(int)
        self.opened: Set[Tuple[int, int]] = set()
        self.flags: Set[Tuple[int, int]] = set()

        self.reset()

    def reset(self) -> None:
        # Set mines
        while len(self.mines) < self.n_mines:
            self.mines.add((
                random.randint(0, self.n_cols - 1),
                random.randint(0, self.n_rows - 1)
            ))
        # Calculate numbers
        for col, row in self.mines:
            for col_, row_ in self.neighbors(col, row):
                if not self.is_mine(col_, row_):
                    self.numbers[(col_, row_)] += 1
        # Others
        self.opened = set()
        self.flags = set()

    def open_(self, col: int, row: int):
        if self.is_open(col, row):
            return

        self.opened.add((col, row))

        if (col, row) in self.flags:
            self.flags.remove((col, row))

        if not self.is_mine(col, row) and self.get_number(col, row) == 0:
            for col_, row_ in self.neighbors(col, row):
                self.open_(col_, row_)

    def toggle_flag(self, col: int, row: int):
        if self.is_open(col, row):
            return

        if (col, row) in self.flags:
            self.flags.remove((col, row))
        else:
            self.flags.add((col, row))

    def neighbors(self, col: int, row: int):
        for dcol, drow in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if dcol == 0 and drow == 0:
                continue
            col_ = col + dcol
            row_ = row + drow
            if not self.is_in_board(col_, row_):
                continue
            yield col_, row_

    def is_in_board(self, col: int, row: int) -> bool:
        return 0 <= col < self.n_cols and 0 <= row < self.n_rows

    def is_open(self, col: int, row: int) -> bool:
        return (col, row) in self.opened

    def is_mine(self, col: int, row: int) -> bool:
        return (col, row) in self.mines

    def is_flag(self, col: int, row: int) -> bool:
        return (col, row) in self.flags

    def get_number(self, col: int, row: int) -> int:
        return self.numbers[(col, row)]

    @property
    def n_cols(self) -> int:
        return self.params.n_cols

    @property
    def n_rows(self) -> int:
        return self.params.n_rows

    @property
    def n_mines(self) -> int:
        return self.params.n_mines

    @property
    def n_flags(self) -> int:
        return len(self.flags)
