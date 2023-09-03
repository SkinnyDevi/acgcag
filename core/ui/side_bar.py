import customtkinter as ctk
from PIL import Image
from pathlib import Path

import core.ui.palette as palette


class SideBar(ctk.CTkFrame):
    def __init__(self, root: ctk.CTk):
        super().__init__(
            root, border_color=palette.BUTTON_BG_GRAY, border_width=2, corner_radius=0
        )

        download_icon = ctk.CTkImage(
            dark_image=Image.open(Path("assets/download-icon.png"))
        )
        downloads_btn = ctk.CTkButton(
            self,
            image=download_icon,
            text="",
            fg_color=palette.MAIN_BEIGE,
            hover_color=palette.DIM_BEIGE,
            width=50,
            height=50,
        )
        downloads_btn.place(x=10, y=50)
        downloads_btn.pack(padx=10, pady=10)

        import_icon = ctk.CTkImage(dark_image=Image.open(Path("assets/banana.png")))
        import_btn = ctk.CTkButton(
            self,
            image=import_icon,
            text="",
            fg_color=palette.MAIN_BEIGE,
            hover_color=palette.DIM_BEIGE,
            width=50,
            height=50,
        )
        import_btn.place(x=10, y=100)
        import_btn.pack(padx=10, pady=10)

    def page_pack(self):
        self.pack(anchor="nw", fill=ctk.BOTH, side=ctk.LEFT)
