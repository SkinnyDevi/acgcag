import tkinter as tk

from core.ui.palette import *


def frame_text(frame: tk.Frame, text: str, font_size: int = 25, **kwargs):
    fg = kwargs.get("fg", DIM_BEIGE)
    bg = kwargs.get("bg", MAIN_GRAY)
    anchor = kwargs.get("anchoer", "e")
    justify = kwargs.get("justify", "left")

    if kwargs.get("fg"):
        del kwargs["fg"]

    if kwargs.get("bg"):
        del kwargs["bg"]

    if kwargs.get("anchor"):
        del kwargs["anchor"]

    if kwargs.get("justify"):
        del kwargs["justify"]

    return tk.Label(
        frame,
        text=text,
        font=APP_FONT(font_size),
        fg=fg,
        bg=bg,
        anchor=anchor,
        justify=justify,
        **kwargs
    )
