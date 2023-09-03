import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers
import core.utils as utils
from core.config.config_manager import ConfigManager
from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.pages.setup_page import SetupPage
from core.ui.pages.main_manager_page import ModManagerPage


class MainApp:
    def __init__(self, root: ctk.CTk):
        CONFIG = ConfigManager.setup()
        CONFIG.clear_cached_previews()

        root.title("ACGCAG")
        utils.set_screen_geometry(root)
        palette.setup_font()
        root.minsize(800, 400)

        if utils.missing_files():
            CONFIG.rerun_setup()

        container = ctk.CTkFrame(
            root,
            fg_color=palette.MAIN_BEIGE if CONFIG.has_run_setup else palette.MAIN_GRAY,
            corner_radius=0,
        )
        container.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)

        title_frame = ctk.CTkFrame(container, corner_radius=0)
        title = ui_helpers.frame_text(
            title_frame,
            "A Certain GUI for a Certain Anime Game",
            25,
            color=palette.MAIN_GRAY if CONFIG.has_run_setup else palette.BRIGHT_BEIGE,
            background=palette.MAIN_BEIGE
            if CONFIG.has_run_setup
            else palette.MAIN_GRAY,
        )
        title.pack()
        title_frame.pack(pady=15, padx=10, side=ctk.TOP, anchor="w")

        self.frames: list[ManagerPageFrame] = [
            SetupPage(container, root),
            ModManagerPage(container),
        ]

        self.frames[0 if CONFIG.has_run_setup else 1].page_forget()
