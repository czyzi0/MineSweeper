import argparse
from collections import defaultdict, namedtuple
from curses import wrapper
from itertools import product
from random import randint


BoardParams = namedtuple('BoardParams', ['x_max', 'y_max', 'n_mines'])


DIFFICULTY_PARAMS = {
    'easy': BoardParams(x_max=9, y_max=9, n_mines=10),
    'intermediate': BoardParams(x_max=16, y_max=16, n_mines=40),
    'expert': BoardParams(x_max=30, y_max=16, n_mines=99),
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
        self.mines: set[tuple[int, int]] = set()
        self.numbers: defaultdict[tuple[int, int], int] = defaultdict(int)
        self.flags: set[tuple[int, int]] = set()

        self.reset()

    def reset(self) -> None:
        # Set mines
        while len(self.mines) < self.params.n_mines:
            self.mines.add((
                randint(0, self.params.x_max - 1),
                randint(0, self.params.y_max - 1)
            ))
        # Calculate numbers
        for x, y in self.mines:
            for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
                x_ = x + dx
                y_ = y + dy
                if self.xy_in_board(x_, y_) and not self.xy_is_mine(x_, y_):
                    self.numbers[(x_, y_)] += 1

    def xy_in_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.params.x_max and 0 <= y < self.params.y_max

    def xy_is_mine(self, x: int, y: int) -> bool:
        return (x, y) in self.mines



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
