import tkinter as tk

import core.ui.palette as palette
import core.ui.components as components


def mount_ui(main_frame: tk.Tk):
    """
    Mounts the UI declared here.
    """

    title_frame = tk.Frame(main_frame)
    title = components.frame_text(
        title_frame,
        "A Certain GUI for a Certain Anime Game",
        18,
        fg=palette.BRIGHT_BEIGE,
    )
    title.pack()
    title_frame.pack(pady=15, padx=10, side=tk.TOP, anchor="w")

    subtitle_frame = tk.Frame(main_frame)
    subtitle = components.frame_text(subtitle_frame, "Downloaded mods", 16)
    subtitle.pack()
    subtitle_frame.pack(pady=0, padx=10, side=tk.TOP, anchor="w")

    mods_frame = tk.Frame(main_frame)

    mod_frame = tk.Frame(mods_frame)
    mod_title = components.frame_text(
        mod_frame,
        "Mod Title",
        24,
    )

    mod_title.pack()
    mod_frame.pack()
    mods_frame.pack(pady=20, padx=10, side=tk.TOP, anchor="w")
