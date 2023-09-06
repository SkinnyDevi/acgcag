import os
import time
import subprocess
import customtkinter as ctk
from PIL import Image
from pathlib import Path
from typing import Callable
from observable import Observable

import core.ui.palette as palette
import core.utils as utils

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
            "download-icon.png",
            lambda: self.__action_page_change("DownloadedModsPage"),
        )

        self.__sidebar_button(
            "banana.png",
            lambda: self.__action_page_change("ImportModsPage"),
        )

        self.__start_btn = self.__sidebar_button(
            "play-icon.png",
            lambda: utils.thread(self.__start_3dmigoto, start=True),
            False,
        )

        self.bind("<Button-1>", lambda x: self.focus())

    def page_pack(self):
        self.pack(anchor="w", fill=ctk.BOTH, side=ctk.LEFT)

    def page_forget(self):
        self.page_forget()

    def __action_page_change(self, page_name: str):
        SideBar.page_change_event.trigger("page_change", page_name)

    def __sidebar_button(self, icon_name: str, action: Callable, above=True):
        btn_icon = self.__btn_icon(icon_name)
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

        return btn

    def __btn_icon(self, icon_name: str):
        return ctk.CTkImage(dark_image=Image.open(Path(f"assets/{icon_name}")))

    def __start_3dmigoto(self):
        # TODO: Upon call, change to page where it waits for genshin to open
        # with a button to finish when genshin and 3dmigoto loads to change screen

        a = subprocess.run(
            'start cmd /k "cd 3dmigoto && call 3dmigoto_loader.exe"', shell=True
        )
        self.__start_btn.configure(image=self.__btn_icon("check-icon.png"))
        time.sleep(5)
        self.__start_btn.configure(image=self.__btn_icon("play-icon.png"))
