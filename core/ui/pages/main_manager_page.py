import customtkinter as ctk

import core.ui.palette as palette

from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.components.side_bar import SideBar

from core.ui.pages.downloaded_page import DownloadedModsPage
from core.ui.pages.import_mods_page import ImportModsPage
from core.ui.pages.skin_config_page import SkinConfigPage
from core.ui.pages.wait_for_genshin_page import WaitForGenshinPage


class ModManagerPage(ManagerPageFrame):
    def __init__(self, parent: ctk.CTkFrame, root: ctk.CTk):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        self.app_root = root

        self.sidebar = SideBar(parent)
        self.page_pack()
        palette.load_background(self._canvas, "app-bg.jpg")

        self.__attach_frames()
        self.__attach_events()
        self.bind("<Button-1>", lambda x: self.focus())

    def __attach_frames(self):
        self.frames: dict[str, ManagerPageFrame] = {}
        self.current_frame: str | None = None

        self.frames[DownloadedModsPage.__name__] = DownloadedModsPage(self)
        self.frames[ImportModsPage.__name__] = ImportModsPage(self, self.app_root)
        self.frames[SkinConfigPage.__name__] = SkinConfigPage(self)
        self.frames[WaitForGenshinPage.__name__] = WaitForGenshinPage(self)

        self.change_page("DownloadedModsPage")

    def __attach_events(self):
        SideBar.page_change_event.on("page_change", lambda p: self.change_page(p))
        SkinConfigPage.page_change_event.on(
            "page_change", lambda p: self.change_page(p)
        )
        WaitForGenshinPage.page_change_event.on(
            "page_change", lambda p: self.change_page(p)
        )

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

        if page_name == WaitForGenshinPage.__name__:
            self.sidebar.state_for_buttons(False)
        elif not self.sidebar.buttons_enabled():
            self.sidebar.state_for_buttons(True)

        page = self.frames[page_name]
        self.current_frame = page_name
        page.page_pack()
