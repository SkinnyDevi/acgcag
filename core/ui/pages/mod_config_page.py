import customtkinter as ctk
from typing import Callable
from observable import Observable

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers

from core.services.local_mod_manager import LocalMod
from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.components.mod_item_frame import ModItemFrame


class ModConfigPage(ManagerPageFrame):
    page_change_event = Observable()
    setup_obs = Observable()

    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        self.__mod_frame = None

        self._title = ui_helpers.frame_text(
            self, "MOD: ", 20, color=palette.BRIGHT_BEIGE
        )
        self._title.pack(pady=10)

        self.__mod_container = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)

        self.__setup_events()
        self.__setup_ui_buttons()

    def page_pack(self):
        self.__setup_mod_frame()
        self.__mod_container.pack(pady=20)
        self.__btns_frame.pack(pady=20)
        self.pack(pady=20)

    def page_forget(self):
        self.forget()
        self.__remove_mod_frame()
        self.__btns_frame.forget()

    def __setup_events(self):
        ModConfigPage.setup_obs.on("set_mod", lambda x: self.__set_mod(x))

    def __set_mod(self, mod: LocalMod):
        self.__mod = mod

        self._title.configure(text=f"MOD: {self.__mod.name.upper()}")
        self.__page_change(ModConfigPage.__name__)

    def __page_change(self, page: str):
        ModConfigPage.page_change_event.trigger("page_change", page)

    def __remove_mod_frame(self):
        if self.__mod_frame is not None:
            self.__mod_frame.destroy()

        self.__mod_frame = None

    def __setup_mod_frame(self):
        self.__mod_frame = ModItemFrame(
            self.__mod_container, self.__mod, manage_button=False
        )
        self.__mod_frame.page_pack()

    def __setup_ui_buttons(self):
        self.__btns_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        self.__ui_button(self.__btns_frame, "Install", lambda: print("Install"))
        self.__ui_button(self.__btns_frame, "Uninstall", lambda: print("Uninstall"))
        self.__ui_button(self.__btns_frame, "Delete", lambda: print("Delete"))
        self.__ui_button(
            self.__btns_frame, "Back", lambda: self.__page_change("DownloadedModsPage")
        )

    def __ui_button(self, parent: ctk.CTkFrame, text: str, cmd: Callable):
        fr = ctk.CTkFrame(parent, fg_color=palette.MAIN_GRAY)
        fr.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")
        btn = ctk.CTkButton(
            fr,
            text=text,
            command=cmd,
            font=palette.APP_FONT(16),
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
        )
        btn.pack(padx=4)

    def __install(self):
        pass

    def __uninstall(self):
        pass

    def __remove(self):
        pass
