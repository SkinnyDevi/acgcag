import tkinter as tk
import customtkinter as ctk
from PIL import Image
from pathlib import Path

import core.utils as utils
import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers

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
        root.resizable(False, False)
        root.iconbitmap(default=Path("assets/app.ico"))

        if utils.missing_files():
            CONFIG.rerun_setup()

        app_bg_color = palette.MAIN_BEIGE if CONFIG.has_run_setup else palette.MAIN_GRAY

        container = ctk.CTkFrame(root, fg_color=app_bg_color, corner_radius=0)
        container.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)

        app_title_frame = ctk.CTkFrame(container, fg_color=app_bg_color)
        app_title_frame.pack(pady=5, padx=5, side=ctk.TOP, anchor="w")

        self.__paimon_icon(app_title_frame, app_bg_color)
        self.__app_title(app_title_frame, app_bg_color, CONFIG)

        self.frames: list[ManagerPageFrame] = [
            SetupPage(container, root),
            ModManagerPage(container, root),
        ]

        self.frames[0 if CONFIG.has_run_setup else 1].page_forget()

    def __paimon_icon(self, container: ctk.CTkFrame, background: str):
        frame = ctk.CTkFrame(container, fg_color=background)
        frame.pack(side=ctk.LEFT, anchor="w", padx=5)

        icon_path = Path("assets/paimon-icon.png")
        raw = Image.open(icon_path)
        img = ctk.CTkImage(dark_image=raw, size=(65, 75))
        icon_label = ctk.CTkLabel(frame, text="", image=img)
        icon_label.pack()

    def __app_title(
        self, container: ctk.CTkFrame, background: str, CONFIG: ConfigManager
    ):
        title_frame = ctk.CTkFrame(container, fg_color=background)
        title_frame.pack(side=ctk.RIGHT, anchor="e", padx=5)

        title = ui_helpers.frame_text(
            title_frame,
            "A Certain GUI for a Certain Anime Game",
            25,
            color=palette.MAIN_GRAY if CONFIG.has_run_setup else palette.BRIGHT_BEIGE,
            background=background,
        )
        title.pack()
