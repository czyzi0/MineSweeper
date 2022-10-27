import curses
import time
from typing import Optional, Tuple

from src.model import MinesweeperModel


class MinesweeperView:

    def __init__(self, model: MinesweeperModel, stdscr):
        self._stdscr = stdscr
        self._model: MinesweeperModel = model

        self._init_curses()

        self._cursor: Tuple[int, int] = (0, 0)
        self._start_time: Optional[float] = None

    def mainloop(self)-> None:
        while True:
            self._print()
            if self._handle_input():
                break

    def _init_curses(self) -> None:
        # Disable cursor
        curses.curs_set(0)
        # No blocking on input
        self._stdscr.nodelay(1)

        # Colors
        ## Non-cursor default
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        ## Non-cursor numbers
        curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(13, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(14, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(16, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(17, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(18, curses.COLOR_GREEN, curses.COLOR_BLACK)
        ## Cursor default
        curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_WHITE)
        ## Cursor numbers
        curses.init_pair(21, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(22, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(23, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(24, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(25, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(26, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(27, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(28, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def _print(self) -> None:
        self._stdscr.clear()

        # Top bar
        self._stdscr.addstr(self._mine_counter_y, self._mine_counter_x, self._mine_counter_value)
        # TODO: emoticon -_-   x_x   ^_^
        self._stdscr.addstr(self._timer_y, self._timer_x, self._timer_value)

        # Board - Box
        self._stdscr.addch(
            self._board_y, self._board_x,
            curses.ACS_ULCORNER)
        self._stdscr.addch(
            self._board_y, self._board_x + self._board_n_cols - 1,
            curses.ACS_URCORNER)
        self._stdscr.addch(
            self._board_y + self._board_n_rows - 1, self._board_x,
            curses.ACS_LLCORNER)
        self._stdscr.addch(
            self._board_y + self._board_n_rows - 1, self._board_x + self._board_n_cols - 1,
            curses.ACS_LRCORNER)
        self._stdscr.hline(
            self._board_y, self._board_x + 1,
            curses.ACS_HLINE, self._board_n_cols - 2)
        self._stdscr.hline(
            self._board_y + self._board_n_rows - 1, self._board_x + 1,
            curses.ACS_HLINE, self._board_n_cols - 2)
        self._stdscr.vline(
            self._board_y + 1, self._board_x,
            curses.ACS_VLINE, self._board_n_rows - 2)
        self._stdscr.vline(
            self._board_y + 1, self._board_x + self._board_n_cols - 1,
            curses.ACS_VLINE, self._board_n_rows - 2)

        # # Board - Fields
        for row in range(self._model.n_rows):
            for col in range(self._model.n_cols):
                is_cursor = self._is_cursor(col, row)
                col_, row_ = self._col_row_model2view(col, row)
                if self._model.is_flag(col, row):
                    self._stdscr.addch(row_, col_, '⚑', self._color(is_cursor))
                elif not self._model.is_revealed(col, row):
                    self._stdscr.addch(row_, col_, '~', self._color(is_cursor))
                elif self._model.is_mine(col, row):
                    self._stdscr.addch(row_, col_, '☀', self._color(is_cursor))
                elif number := self._model.get_number(col, row):
                    self._stdscr.addch(row_, col_, str(number), self._color(is_cursor, number))
                else:
                    self._stdscr.addch(row_, col_, ' ', self._color(is_cursor))

        self._stdscr.refresh()

    @property
    def _mine_counter_x(self) -> int:
        return 0

    @property
    def _mine_counter_y(self) -> int:
        return 0

    @property
    def _mine_counter_value(self) -> str:
        return f'{self._model.n_mines - self._model.n_flags:03}'

    @property
    def _timer_x(self) -> int:
        return self._board_n_cols - 3

    @property
    def _timer_y(self) -> int:
        return 0

    @property
    def _timer_value(self) -> str:
        if self._start_time is None:
            return '000'
        return f'{min(999, int(time.time() - self._start_time)):03}'

    @property
    def _board_x(self) -> int:
        return 0

    @property
    def _board_y(self) -> int:
        return 1

    @property
    def _board_n_cols(self) -> int:
        return 2 * self._model.n_cols + 1

    @property
    def _board_n_rows(self) -> int:
        return self._model.n_rows + 2

    def _is_cursor(self, col: int, row: int) -> bool:
        # TODO: If lost, everything is not a cursor
        return (col, row) == self._cursor

    def _col_row_model2view(self, col: int, row: int) -> Tuple[int, int]:
        col = self._board_x + 1 + 2 * col
        row = self._board_y + 1 + row
        return col, row

    def _color(self, is_cursor: bool, number: int = 0) -> int:
        return curses.color_pair(20 + number if is_cursor else 10 + number)

    def _handle_input(self) -> bool:
        try:
            key = self._stdscr.getkey()
        except curses.error:
            time.sleep(0.1)
            key = None

        if key in ('q', 'Q'):
            return True

        # TODO: Check win condition

        elif key == 'KEY_UP':
            self._move_cursor(0, -1)
        elif key == 'KEY_DOWN':
            self._move_cursor(0, 1)
        elif key == 'KEY_LEFT':
            self._move_cursor(-1, 0)
        elif key == 'KEY_RIGHT':
            self._move_cursor(1, 0)

        elif key == ' ':
            self._start_timer()
            self._model.reveal(*self._cursor)

        elif key in ('f', 'F'):
            self._start_timer()
            self._model.toggle_flag(*self._cursor)

        return False

    def _move_cursor(self, dcol: int, drow: int) -> None:
        col, row = self._cursor
        col += dcol
        row += drow
        if self._model.is_in_board(col, row):
            self._cursor = (col, row)

    def _start_timer(self) -> None:
        if self._start_time is None:
            self._start_time = time.time()
