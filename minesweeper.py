import argparse
import curses
from collections import defaultdict, namedtuple
from itertools import product
from random import randint
from typing import DefaultDict, Dict, Set, Tuple


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

        # for col in range(self.n_cols):
        #     for row in range(self.n_rows):
        #         self.opened.add((col, row))

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

    def is_open(self, col: int, row: int) -> bool:
        return (col, row) in self.opened

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
        curses.curs_set(0)

        self.stdscr = stdscr
        self.init_colors()

        self.model = model

        self.cursor = (0, 0)

    def mainloop(self)-> None:
        while True:
            self.stdscr.clear()

            for row in range(self.model.n_rows):
                for col in range(self.model.n_cols):
                    is_cursor = self.is_cursor(col, row)
                    if not self.model.is_open(col, row):
                        self.stdscr.addch(row, 2 * col, '~', self.get_color(is_cursor))
                    elif self.model.is_mine(col, row):
                        self.stdscr.addch(row, 2 * col, 'X', self.get_color(is_cursor))
                    elif number := self.model.get_number(col, row):
                        self.stdscr.addch(row, 2 * col, str(number), self.get_color(is_cursor, number))
                    else:
                        self.stdscr.addch(row, 2 * col, ' ', self.get_color(is_cursor))

            self.stdscr.refresh()

            key = self.stdscr.getkey()

            if key == 'q' or key == 'Q':
                break

            if key == 'KEY_UP':
                self.cursor = (self.cursor[0], max(0, self.cursor[1] - 1))
                continue
            if key == 'KEY_DOWN':
                self.cursor = (self.cursor[0], min(self.model.n_rows - 1, self.cursor[1] + 1))
                continue
            if key == 'KEY_LEFT':
                self.cursor = (max(0, self.cursor[0] - 1), self.cursor[1])
                continue
            if key == 'KEY_RIGHT':
                self.cursor = (min(self.model.n_cols - 1, self.cursor[0] + 1), self.cursor[1])
                continue

    def init_colors(self) -> None:
        # Non-cursor default
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Non-cursor numbers
        curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(13, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(14, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(16, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(17, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(18, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Cursor default
        curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_WHITE)
        # Cursor numbers
        curses.init_pair(21, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(22, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(23, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(24, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(25, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(26, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(27, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(28, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def get_color(self, is_cursor: bool, number: int = 0) -> int:
        return curses.color_pair(20 + number if is_cursor else 10 + number)

    def is_cursor(self, col: int, row: int) -> bool:
        return (col, row) == self.cursor


def main(stdscr, difficulty):
    MinesweeperView(
        MinesweeperModel(DIFFICULTY_PARAMS[difficulty]),
        stdscr
    ).mainloop()


if __name__ == '__main__':
    args = parse_args()
    curses.wrapper(main, difficulty=args.difficulty)
