import customtkinter as ctk
from PIL import Image
from pathlib import Path
from typing import Callable
from observable import Observable

import core.ui.palette as palette

from core.ui.components.custom_frame import ManagerPageFrame


class SideBar(ManagerPageFrame):
    page_change_event = Observable()

    def __init__(self, root: ctk.CTk):
        super().__init__(
            root,
            fg_color=palette.MENU_BACKGROUND,
            corner_radius=0,
        )

        self.__sidebar_button(
            Path("assets/download-icon.png"),
            lambda: self.__action_page_change("DownloadedModsPage"),
        )

        self.__sidebar_button(
            Path("assets/banana.png"),
            lambda: self.__action_page_change("ImportModsPage"),
        )

        self.bind("<Button-1>", lambda x: self.focus())

    def page_pack(self):
        self.pack(anchor="w", fill=ctk.BOTH, side=ctk.LEFT)

    def page_forget(self):
        self.page_forget()

    def __action_page_change(self, page_name: str):
        SideBar.page_change_event.trigger("page_change", page_name)

    def __sidebar_button(self, image_path: Path, action: Callable, above=True):
        btn_icon = ctk.CTkImage(dark_image=Image.open(image_path))
        btn = ctk.CTkButton(
            self,
            image=btn_icon,
            text="",
            fg_color=palette.BUTTON_BACKGROUND,
            hover_color=palette.DIM_BEIGE,
            width=50,
            height=50,
            command=action,
        )
        btn.place(x=100)
        btn.pack(padx=10, pady=10, side=ctk.TOP if above else ctk.BOTTOM)
        btn.bind("<Button-1>", lambda x: self.focus())
