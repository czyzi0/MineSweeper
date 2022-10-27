import curses
import time
from typing import Optional

from src.model import MinesweeperModel


class MinesweeperView:

    def __init__(self, model: MinesweeperModel, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(1)
        self.init_colors()

        self.stdscr = stdscr
        self.model = model

        self.cursor = (0, 0)
        self.start_time: Optional[float] = None

    def mainloop(self)-> None:
        finished = False
        while not finished:
            self.print_scr()
            finished = self.handle_ctrl()

    def print_scr(self) -> None:
        self.stdscr.clear()

        board_n_cols = 2 * self.model.n_cols + 1
        board_n_rows = self.model.n_rows + 2

        # Mines counter
        self.stdscr.addstr(0, 0, self.get_mines_counter_value())
        # Emoticon
        # TODO
        # -_-   x_x   ^_^
        # Timer
        self.stdscr.addstr(0, board_n_cols - 3, self.get_timer_value())

        # Board
        ## Box
        self.stdscr.hline(1, 1, curses.ACS_HLINE, board_n_cols - 2)
        self.stdscr.hline(1 + board_n_rows - 1, 1, curses.ACS_HLINE, board_n_cols - 2)
        self.stdscr.vline(2, 0, curses.ACS_VLINE, board_n_rows - 2)
        self.stdscr.vline(2, board_n_cols - 1, curses.ACS_VLINE, board_n_rows - 2)
        self.stdscr.addch(1, 0, curses.ACS_ULCORNER)
        self.stdscr.addch(1, board_n_cols - 1, curses.ACS_URCORNER)
        self.stdscr.addch(1 + board_n_rows - 1, 0, curses.ACS_LLCORNER)
        self.stdscr.addch(1 + board_n_rows - 1, board_n_cols - 1, curses.ACS_LRCORNER)
        ## Fields
        for row in range(self.model.n_rows):
            for col in range(self.model.n_cols):
                is_cursor = self.is_cursor(col, row)
                if self.model.is_flag(col, row):
                    self.stdscr.addch(2 + row, 2 * col + 1, '⚑', self.get_color(is_cursor))
                elif not self.model.is_open(col, row):
                    self.stdscr.addch(2 + row, 2 * col + 1, '~', self.get_color(is_cursor))
                elif self.model.is_mine(col, row):
                    self.stdscr.addch(2 + row, 2 * col + 1, '☀', self.get_color(is_cursor))
                elif number := self.model.get_number(col, row):
                    self.stdscr.addch(
                        2 + row, 2 * col + 1, str(number), self.get_color(is_cursor, number))
                else:
                    self.stdscr.addch(2 + row, 2 * col + 1, ' ', self.get_color(is_cursor))

        # Help
        self.stdscr.addstr(1 + board_n_rows, 0, 'Navigate: ← → ↑ ↓')
        self.stdscr.addstr(1 + board_n_rows + 1, 0, 'Open: Space')
        self.stdscr.addstr(1 + board_n_rows + 2, 0, 'Flag: f')
        self.stdscr.addstr(1 + board_n_rows + 3, 0, 'Exit: q')

        self.stdscr.refresh()

    def handle_ctrl(self) -> bool:
        try:
            key = self.stdscr.getkey()
        except curses.error:
            time.sleep(0.1)
            key = None

        if key in ('q', 'Q'):
            return True

        elif key == 'KEY_UP':
            self.cursor = (self.cursor[0], max(0, self.cursor[1] - 1))
        elif key == 'KEY_DOWN':
            self.cursor = (self.cursor[0], min(self.model.n_rows - 1, self.cursor[1] + 1))
        elif key == 'KEY_LEFT':
            self.cursor = (max(0, self.cursor[0] - 1), self.cursor[1])
        elif key == 'KEY_RIGHT':
            self.cursor = (min(self.model.n_cols - 1, self.cursor[0] + 1), self.cursor[1])

        elif key == ' ':
            self.start_timer()
            if not self.model.is_flag(*self.cursor):
                self.model.open_(*self.cursor)

        elif key in ('f', 'F'):
            self.start_timer()
            self.model.toggle_flag(*self.cursor)

        # TODO: Check if lost

        return False

    def get_color(self, is_cursor: bool, number: int = 0) -> int:
        return curses.color_pair(20 + number if is_cursor else 10 + number)

    def is_cursor(self, col: int, row: int) -> bool:
        # TODO: If lost, everything is not a cursor
        return (col, row) == self.cursor

    def get_mines_counter_value(self) -> str:
        mines_counter_value = self.model.n_mines - self.model.n_flags
        return f'{mines_counter_value:03}'

    def get_timer_value(self) -> str:
        if self.start_time is None:
            return '000'
        timer_value = min(999, int(time.time() - self.start_time))
        return f'{timer_value:03}'

    def start_timer(self) -> None:
        if self.start_time is None:
            self.start_time = time.time()

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
