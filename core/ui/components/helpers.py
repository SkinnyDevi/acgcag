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


def frame_left_aligned(parent: ctk.CTkFrame, **kwargs):
    frame = ctk.CTkFrame(parent, **kwargs)
    frame.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")
    return frame


def label_left_aligned(parent: ctk.CTkFrame, title: str, font_size=18):
    title_frame = ctk.CTkFrame(parent)
    title_text = frame_text(
        title_frame,
        title,
        font_size,
    )
    title_text.pack()
    title_frame.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")

    return title_frame, title_text
