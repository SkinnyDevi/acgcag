import customtkinter as ctk

from core.ui.palette import *


def frame_text(
    frame: ctk.CTkFrame,
    text: str,
    font_size: int = 15,
    *,
    color=DIM_BEIGE,
    background=MAIN_GRAY,
    anchor="e",
    justify="left",
    **kwargs
):
    label = ctk.CTkLabel(
        frame,
        text=text,
        font=APP_FONT(font_size),
        text_color=color,
        bg_color=background,
        anchor=anchor,
        **kwargs,
    )

    label._label.configure(justify=justify)
    return label
