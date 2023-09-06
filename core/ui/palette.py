"""
Constants for storing colours for the UI.
"""

import customtkinter as ctk
from pathlib import Path

MENU_BACKGROUND = "#3d4557"
BUTTON_BACKGROUND = "#dad5cb"
TEXT_COLOR_DARK = "#3d4557"
WHITE = "#ffffff"
MAIN_BEIGE = "#ece5d8"
BRIGHT_BEIGE = "#d3bc8f"
DIM_BEIGE = "#b0a17d"
MAIN_GRAY = "#1d1c21"
LESSER_GRAY = "#312f37"
VARIANT_GRAY = "#495366"


def setup_font():
    """
    Allows the use of the app font inside the program.
    """
    path = Path("assets/fonts/app-font.ttf")
    font = str(path.absolute())
    ctk.FontManager.load_font(font)


def APP_FONT(size: int):
    """
    Returns the app font with the specified size.
    """
    return ("HYWenHei-85W", size, "normal")


def load_background(component: ctk.CTkCanvas, name: str):
    from PIL import Image, ImageEnhance, ImageFilter, ImageTk

    image = Image.open(Path(f"assets/backgrounds/{name}"))
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.5)
    image = image.filter(ImageFilter.BoxBlur(20))

    bg = ctk.CTkImage(dark_image=image, size=(1300, 800))
    bg_label = ctk.CTkLabel(component, text="", image=bg)
    bg_label.place(x=0, y=0, anchor="nw")
