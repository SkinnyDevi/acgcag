import customtkinter as ctk

from core.ui.palette import *


def frame_text(
    frame: ctk.CTkFrame,
    text: str,
    font_size: int = 25,
    *,
    color=DIM_BEIGE,
    background=MAIN_GRAY,
    anchor="e",
    justify="left",
    **kwargs
):
    return ctk.CTkLabel(
        frame,
        text=text,
        font=APP_FONT(font_size),
        text_color=color,
        bg_color=background,
        anchor=anchor,
        compound=justify,
        **kwargs
    )
