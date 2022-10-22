import argparse
from collections import defaultdict, namedtuple
from curses import wrapper
from itertools import product
from random import randint
from typing import DefaultDict, Set, Tuple


BoardParams = namedtuple('BoardParams', ['n_cols', 'n_rows', 'n_mines'])


DIFFICULTY_PARAMS = {
    'easy': BoardParams(n_cols=9, n_rows=9, n_mines=10),
    'intermediate': BoardParams(n_cols=16, n_rows=16, n_mines=40),
    'expert': BoardParams(n_cols=30, n_rows=16, n_mines=99),
}


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
        '-d', '--difficulty', type=str,
        default=list(DIFFICULTY_PARAMS.keys())[0], choices=DIFFICULTY_PARAMS.keys(),
        help=''
    )

    return parser.parse_args()


class Board:

    def __init__(self, params: BoardParams):
        self.params: BoardParams = params
        self.mines: Set[Tuple[int, int]] = set()
        self.numbers: DefaultDict[Tuple[int, int], int] = defaultdict(int)
        self.opened: Set[Tuple[int, int]] = set()
        self.flags: Set[Tuple[int, int]] = set()

        self.reset()

    def reset(self) -> None:
        # Set mines
        while len(self.mines) < self.params.n_mines:
            self.mines.add((
                randint(0, self.params.n_cols - 1),
                randint(0, self.params.n_rows - 1)
            ))
        # Calculate numbers
        for col, row in self.mines:
            for col_, row_ in self.neighbors(col, row):
                if not self.is_mine(col_, row_):
                    self.numbers[(col_, row_)] += 1
        # Others
        self.opened = set()
        self.flags = set()

    def open(self, col: int, row: int):
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
        return 0 <= col < self.params.n_cols and 0 <= row < self.params.n_rows

    def is_mine(self, col: int, row: int) -> bool:
        return (col, row) in self.mines


def main_(difficulty):
    print('Hello, World!')
    print(difficulty)

    board = Board(DIFFICULTY_PARAMS[difficulty])
    print(board.mines)
    print(board.numbers)


def main(stdscr, difficulty):
    stdscr.clear()

    stdscr.addstr(difficulty)

    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    args = parse_args()
    main_(args.difficulty)
    #wrapper(main, difficulty=args.difficulty)
