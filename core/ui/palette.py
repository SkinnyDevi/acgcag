"""
Constants for storing colours for the UI.
"""

import customtkinter as ctk
from pathlib import Path

WHITE = "#ffffff"
MAIN_GRAY = "#1d1c21"
BUTTON_BG_GRAY = "#495366"
MAIN_BEIGE = "#ece5d8"
BRIGHT_BEIGE = "#d3bc8f"
DIM_BEIGE = "#b0a17d"


def setup_font():
    """
    Allows the use of the app font inside the program.
    """
    path = Path("assets/app-font.ttf")

    font = str(path.absolute())
    ctk.FontManager.load_font(font)


def APP_FONT(size: int):
    """
    Returns the app font with the specified size.
    """
    return ("HYWenHei-85W", size, "normal")
