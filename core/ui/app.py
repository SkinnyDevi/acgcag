import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components as components
import core.utils as utils
from core.config.config_manager import ConfigManager
from core.ui.side_bar import SideBar
from core.ui.setup_page import SetupPage
from core.ui.mod_manager_page import ModManagerPage


class MainApp:
    def __init__(self, root: ctk.CTk):
        CONFIG = ConfigManager.setup()

        root.title("ACGCAG")
        utils.set_screen_geometry(root)
        palette.setup_font()
        root.minsize(500, 200)

        sidebar = SideBar(root)
        if CONFIG.has_run_setup:
            sidebar.pack()

        container = ctk.CTkFrame(root, fg_color=palette.MAIN_GRAY)
        container.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)

        title_frame = ctk.CTkFrame(container)
        title = components.frame_text(
            title_frame,
            "A Certain GUI for a Certain Anime Game",
            20,
            color=palette.BRIGHT_BEIGE,
        )
        title.pack()
        title_frame.pack(pady=15, padx=10, side=ctk.TOP, anchor="w")

        self.frames: dict[str, ctk.CTkFrame] = {
            SetupPage.__name__: SetupPage(container, root),
            ModManagerPage.__name__: ModManagerPage(container),
        }

        self.frames["ModManagerPage"].forget()
