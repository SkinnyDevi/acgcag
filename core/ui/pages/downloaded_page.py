import customtkinter as ctk

import core.utils as utils
import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers

from core.services.local_mod_manager import LocalMod, LocalModManager
from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.components.mod_item_frame import ModItemFrame
from core.ui.pages.mod_config_page import ModConfigPage


class DownloadedModsPage(ManagerPageFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.__mm = LocalModManager()

        self.__scrollframe = ctk.CTkScrollableFrame(
            self, 1125, 540, fg_color=palette.MAIN_GRAY
        )

        ui_helpers.frame_text(
            self, "DOWNLOADED MODS", 20, color=palette.BRIGHT_BEIGE
        ).pack(pady=10)

        self.__mod_frames: list[ctk.CTkFrame] = []

    def page_pack(self):
        self.__populate_mods()
        self.__scrollframe.pack()
        self.pack(pady=10)

    def page_forget(self):
        self.__safely_remove_scroller()
        self.__scrollframe.forget()
        self.forget()

    def __populate_mods(self):
        self.__mm.refresh()
        for x, y, z in utils.triplets_of(self.__mm.mods):
            self.__mod_row(x, y, z)

    def __safely_remove_scroller(self):
        for m in self.__mod_frames:
            m.destroy()

        self.__mod_frames.clear()

    def __mod_row(self, mod1: LocalMod, mod2: LocalMod = None, mod3: LocalMod = None):
        frame = ctk.CTkFrame(self.__scrollframe, fg_color=palette.MAIN_GRAY)
        frame.pack(anchor="w")

        self.__new_mod_item_frame(frame, mod1).page_pack()
        if mod2 is not None:
            self.__new_mod_item_frame(frame, mod2).page_pack()
        if mod3 is not None:
            self.__new_mod_item_frame(frame, mod3).page_pack()

        self.__mod_frames.append(frame)

    def __new_mod_item_frame(self, frame: ctk.CTkFrame, mod: LocalMod):
        return ModItemFrame(
            frame,
            mod,
            lambda: self.__open_manager_page(mod),
            display_installed=True,
        )

    def __open_manager_page(self, mod: LocalMod):
        ModConfigPage.setup_obs.trigger("set_mod", mod)
