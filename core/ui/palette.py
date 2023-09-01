"""
Constants for storing colours for the UI.
"""

import tkinter.font as tkfont
import pyglet
from pathlib import Path

MAIN_GRAY = "#1d1c21"
BRIGHT_BEIGE = "#d3bc8f"
DIM_BEIGE = "#b0a17d"


def setup_font():
    """
    Allows the use of the app font inside the program.
    """

    with open(Path("assets/app-font.ttf"), "rb") as font:
        pyglet.font.add_file(font)


def APP_FONT(size: int):
    """
    Returns the app font with the specified size.
    """
    return tkfont.Font(font=("HYWenHei", size, "normal"))
