import customtkinter as ctk
from PIL import Image
from pathlib import Path
from observable import Observable

import core.ui.palette as palette
from core.ui.components.custom_frame import ManagerPageFrame


class SideBar(ManagerPageFrame):
    page_change_event = Observable()

    def __init__(self, root: ctk.CTk):
        super().__init__(
            root,
            fg_color=palette.MAIN_GRAY,
            border_color=palette.BRIGHT_BEIGE,
            border_width=2,
        )

        download_icon = ctk.CTkImage(
            dark_image=Image.open(Path("assets/download-icon.png"))
        )
        downloads_btn = ctk.CTkButton(
            self,
            image=download_icon,
            text="",
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
            width=50,
            height=50,
            command=lambda: self.action_page_change("DownloadedModsPage"),
        )
        downloads_btn.place(x=10, y=50)
        downloads_btn.pack(padx=10, pady=10)

        import_icon = ctk.CTkImage(dark_image=Image.open(Path("assets/banana.png")))
        import_btn = ctk.CTkButton(
            self,
            image=import_icon,
            text="",
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
            width=50,
            height=50,
            command=lambda: self.action_page_change("ImportModsPage"),
        )
        import_btn.place(x=10, y=100)
        import_btn.pack(padx=10, pady=10)

    def page_pack(self):
        self.pack(anchor="nw", fill=ctk.BOTH, side=ctk.LEFT)

    def page_forget(self):
        self.page_forget()

    def action_page_change(self, page_name: str):
        SideBar.page_change_event.trigger("page_change", page_name)
