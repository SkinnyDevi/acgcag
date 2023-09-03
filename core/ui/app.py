import sys
import os
import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components as components
import core.utils as utils
from core.config.config_manager import ConfigManager
from core.ui.custom_frame import ManagerPageFrame
from core.ui.setup_page import SetupPage
from core.ui.mod_manager_page import ModManagerPage


class MainApp:
    def __init__(self, root: ctk.CTk):
        CONFIG = ConfigManager.setup()

        root.title("ACGCAG")
        utils.set_screen_geometry(root)
        palette.setup_font()
        root.minsize(500, 200)

        if utils.missing_files():
            CONFIG.rerun_setup()

        container = ctk.CTkFrame(root, fg_color=palette.BRIGHT_BEIGE)
        container.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)

        title_frame = ctk.CTkFrame(container, corner_radius=0)
        title = components.frame_text(
            title_frame,
            "A Certain GUI for a Certain Anime Game",
            20,
            color=palette.MAIN_GRAY,
            background=palette.BRIGHT_BEIGE,
        )
        title.pack()
        title_frame.pack(pady=15, padx=10, side=ctk.TOP, anchor="w")

        self.frames: list[ManagerPageFrame] = [
            SetupPage(container, root),
            ModManagerPage(container),
        ]

        self.frames[0 if CONFIG.has_run_setup else 1].page_forget()
