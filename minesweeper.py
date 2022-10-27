import argparse
import curses

from src.model import MinesweeperModel, MinesweeperParams
from src.view import MinesweeperView


DIFFICULTY_PARAMS = {
    'easy': MinesweeperParams(n_cols=9, n_rows=9, n_mines=10),
    'intermediate': MinesweeperParams(n_cols=16, n_rows=16, n_mines=40),
    'expert': MinesweeperParams(n_cols=30, n_rows=16, n_mines=99),
}


def parse_args():
    parser = argparse.ArgumentParser(description= \
        f'Play Minesweeper game. To navigate use ← → ↑ ↓, to reveal a field press Space, ' \
        f'to flag a field use f and to quit the game press q.')

    parser.add_argument(
        '-d', '--difficulty', type=str,
        default=list(DIFFICULTY_PARAMS.keys())[0], choices=DIFFICULTY_PARAMS.keys(),
        help='choose difficulty level'
    )

    return parser.parse_args()


def main(stdscr, difficulty):
    MinesweeperView(
        MinesweeperModel(DIFFICULTY_PARAMS[difficulty]),
        stdscr
    ).mainloop()


if __name__ == '__main__':
    args = parse_args()
    curses.wrapper(main, difficulty=args.difficulty)
