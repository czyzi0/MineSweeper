import argparse
import curses
from collections import defaultdict, namedtuple
from itertools import product
from random import randint
from typing import DefaultDict, Set, Tuple


Params = namedtuple('Params', ['n_cols', 'n_rows', 'n_mines'])


DIFFICULTY_PARAMS = {
    'easy': Params(n_cols=9, n_rows=9, n_mines=10),
    'intermediate': Params(n_cols=16, n_rows=16, n_mines=40),
    'expert': Params(n_cols=30, n_rows=16, n_mines=99),
}


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
        '-d', '--difficulty', type=str,
        default=list(DIFFICULTY_PARAMS.keys())[0], choices=DIFFICULTY_PARAMS.keys(),
        help=''
    )

    return parser.parse_args()


class MinesweeperModel:

    def __init__(self, params: Params):
        self.params: Params = params

        self.mines: Set[Tuple[int, int]] = set()
        self.numbers: DefaultDict[Tuple[int, int], int] = defaultdict(int)
        self.opened: Set[Tuple[int, int]] = set()
        self.flags: Set[Tuple[int, int]] = set()

        self.reset()

    def reset(self) -> None:
        # Set mines
        while len(self.mines) < self.n_mines:
            self.mines.add((
                randint(0, self.n_cols - 1),
                randint(0, self.n_rows - 1)
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
        pass

    def neighbors(self, col: int, row: int):
        for dcol, drow in product([-1, 0, 1], [-1, 0, 1]):
            if dcol == 0 and drow == 0:
                continue
            col_ = col + dcol
            row_ = row + drow
            if not self.is_in_board(col_, row_):
                continue
            yield col_, row_

    def is_in_board(self, col: int, row: int) -> bool:
        return 0 <= col < self.n_cols and 0 <= row < self.n_rows

    def is_mine(self, col: int, row: int) -> bool:
        return (col, row) in self.mines

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


class MinesweeperView:

    def __init__(self, model: MinesweeperModel, stdscr):
        self.model = model

        self.stdscr = stdscr

    def mainloop(self)-> None:
        self.stdscr.clear()

        for row in range(self.model.n_rows):
            for col in range(self.model.n_cols):
                if self.model.is_mine(col, row):
                    self.stdscr.addch(row, 2 * col, 'o')
                elif number := self.model.get_number(col, row):
                    self.stdscr.addch(row, 2 * col, str(number))


        self.stdscr.refresh()
        self.stdscr.getkey()


def main(stdscr, difficulty):
    curses.curs_set(0)

    MinesweeperView(
        MinesweeperModel(DIFFICULTY_PARAMS[difficulty]),
        stdscr
    ).mainloop()


if __name__ == '__main__':
    args = parse_args()
    curses.wrapper(main, difficulty=args.difficulty)
