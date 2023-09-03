import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components as components
from core.ui.custom_frame import ManagerPageFrame
from core.ui.side_bar import SideBar


class ModManagerPage(ManagerPageFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, fg_color=palette.MAIN_GRAY, corner_radius=0)

        self.sidebar = SideBar(parent)
        components.frame_text(self, "MOD MANAGER", 16).pack()
        self.page_pack()

        self.frames: dict[str, ctk.CTkFrame] = {}

    def page_pack(self):
        self.sidebar.page_pack()
        self.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)

    def page_forget(self):
        self.sidebar.forget()
        self.forget()

    def change_page(self, page_name: str):
        """
        Change the page displayed in the app.
        """

        for page in self.frames.values():
            page.forget()

        if page_name not in self.frames.keys():
            raise RuntimeError(f"No page in the app named '{page_name}'")

        page = self.frames[page_name]
        page.tkraise()
        page.page_pack()
