import customtkinter as ctk

import core.ui.palette as palette
from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.components.side_bar import SideBar

from core.ui.pages.downloaded_page import DownloadedModsPage
from core.ui.pages.import_mods_page import ImportModsPage


class ModManagerPage(ManagerPageFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(
            parent,
            fg_color=palette.MAIN_GRAY,
            border_color=palette.MAIN_BEIGE,
            border_width=2,
        )

        self.sidebar = SideBar(parent)
        self.page_pack()

        self.frames: dict[str, ManagerPageFrame] = {}
        self.current_frame: str | None = None

        self.frames[DownloadedModsPage.__name__] = DownloadedModsPage(self)
        self.frames[ImportModsPage.__name__] = ImportModsPage(self)

        self.change_page("DownloadedModsPage")

        SideBar.page_change_event.on("page_change", lambda p: self.change_page(p))

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

        if self.current_frame == page_name:
            return

        for page in self.frames.values():
            page.page_forget()

        if page_name not in self.frames.keys():
            raise RuntimeError(f"No page in the app named '{page_name}'")

        page = self.frames[page_name]
        self.current_frame = page_name
        page.tkraise()
        page.page_pack()
