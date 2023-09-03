import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers
from core.ui.components.custom_frame import ManagerPageFrame


class DownloadedModsPage(ManagerPageFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        title = ui_helpers.frame_text(
            self, "DOWNLOADED MODS", 20, color=palette.BRIGHT_BEIGE
        )
        title.pack(pady=10)

    def page_pack(self):
        self.pack(pady=10)

    def page_forget(self):
        self.forget()
