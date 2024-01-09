from sys import stdin, stdout
from typing import Literal

from . import read, read_ready

CURSOR_MODE = {
    "user": 0,
    "blink_block": 1,
    "blick_under": 3,
    "blink_bar": 5,
    "steady_block": 2,
    "steady_under": 4,
    "steady_bar": 6,
}


class Cursor:
    """Representation of the terminal cursor."""

    @staticmethod
    def up(count: int = 1) -> None:
        """Move the cursor up by {count} lines."""
        stdout.write(f"\x1b[{count}A")
        stdout.flush()

    @staticmethod
    def down(count: int = 1) -> None:
        """Move the cursor down by {count} lines."""
        stdout.write(f"\x1b[{count}B")
        stdout.flush()

    @staticmethod
    def left(count: int = 1) -> None:
        """Move the cursor left by {count} columns."""
        stdout.write(f"\x1b[{count}C")
        stdout.flush()

    @staticmethod
    def right(count: int = 1) -> None:
        """Move the cursor right by {count} columns."""
        stdout.write(f"\x1b[{count}D")
        stdout.flush()

    @staticmethod
    def move(x: int = 0, y: int = 0) -> None:
        """Move cursor to the specified x and/or y position.

        Call with no args or with 0, 0 to execute the `home` command; `\\x1b[H`
        """
        if x is None and y is None:
            stdout.write("\x1b[H")
        elif x is None and y is not None:
            stdout.write(f"\x1b[{y}d")
        elif x is not None and y is None:
            stdout.write(f"\x1b[{x}G")
        else:
            stdout.write(f"\x1b[{y};{x}H")
        stdout.flush()

    @staticmethod
    def save() -> None:
        """Save the cursors current position."""
        stdout.write("\x1b[s")
        stdout.flush()

    @staticmethod
    def load() -> None:
        """Load the cursors previous position."""
        stdout.write("\x1b[u")
        stdout.flush()

    @staticmethod
    def delete(count: int = 1) -> None:
        """Delete {count} characters."""
        stdout.write(f"\x1b[{count}P")
        stdout.flush()

    @staticmethod
    def erase(count: int = 1) -> None:
        """Erase {count} characters.

        Replaces them with ` `
        """
        stdout.write(f"\x1b[{count}X")
        stdout.flush()

    @staticmethod
    def del_line(count: int = 1) -> None:
        """Delete {count} lines starting from the cursors current position."""
        stdout.write(f"\x1b[{count}M")
        stdout.flush()

    @staticmethod
    def insert_line(count: int = 1) -> None:
        """Insert blank lines starting from the cursors current position.
        This includes the line the cursor is currently on.
        """
        stdout.write(f"\x1b[{count}L")
        stdout.flush()

    @staticmethod
    def show() -> None:
        """Show the cursor."""
        stdout.write("\x1b[25h")
        stdout.flush()

    @staticmethod
    def hide() -> None:
        """Show the cursor."""
        stdout.write("\x1b[25l")
        stdout.flush()

    @staticmethod
    def mode(
        mode: Literal[
            "user",
            "blink_block",
            "blick_under",
            "blink_bar",
            "steady_block",
            "steady_under",
            "steady_bar",
        ],
    ) -> None:
        """Change the cursor mode. Defaults to `user`"""
        stdout.write(f"\x1b[{CURSOR_MODE[mode]}q")
        stdout.flush()

    @staticmethod
    def pos() -> tuple[int, int]:
        """Get the cursors position. (x, y)

        Returns:
            (int, int): The x and y coordinates of the cursor.
        """
        stdout.write("\x1b[6n")
        stdout.flush()

        # Collect input which could be blank meaning no ansi input
        char = ""
        try:
            char += read(1)
            while read_ready(stdin):
                char += read(1)
        finally:
            pass

        char = char.lstrip("\x1b[").rstrip("R")
        y, x = char.split(";")
        return int(x), int(y)


class Terminal:
    """Represents the terminal window."""

    @staticmethod
    def clear(mode: Literal["start", "cursor", "entire"] = "entire") -> None:
        """Erase the display with the given method.

        Modes:
            start: Erase from start of display to cursor
            cursor: Erase from cursor to end of display
            entire: Erase entire display
        """
        if mode == "start":
            mode = 0
        elif mode == "cursor":
            mode = 1
        elif mode == "entire":
            mode = 2
        else:
            return

        stdout.write(f"\x1b[{mode}J")
        stdout.flush()

    @staticmethod
    def title(title: str = "") -> None:
        """Set the terminal title."""
        stdout.write(f"\x1b]0;{title}\x07")
        stdout.flush()
