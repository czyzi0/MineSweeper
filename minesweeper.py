import argparse
from functools import partial
from curses import wrapper


def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--size', type=int, default=10, help='')

    return parser.parse_args()


def main(stdscr, size):
    stdscr.clear()

    stdscr.addstr(str(size))

    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    args = parse_args()
    wrapper(partial(main, size=args.size))
