import contextlib
import customtkinter as ctk
from zipfile import BadZipFile
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
        self.__setup_installed_text()
        self.__setup_ui_buttons()

    def page_pack(self):
        self.__setup_mod_frame()
        self.__mod_container.pack(pady=20)
        self.__installed_text_frame.pack(pady=10)
        self.__btns_frame.pack(pady=20)
        self.pack(pady=20)

    def page_forget(self):
        self.forget()
        self.__remove_mod_frame()
        self.__btns_frame.forget()
        self.__reset_buttons()

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
        self.__installed_text_frame.forget()

    def __setup_mod_frame(self):
        self.__mod_frame = ModItemFrame(
            self.__mod_container, self.__mod, manage_button=False
        )
        self.__mod_frame.page_pack()
        self.__installed_text.configure(
            text=f"Is installed: {'Yes' if self.__mod.is_installed else 'No'}"
        )

    def __setup_installed_text(self):
        self.__installed_text_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        self.__installed_text = ui_helpers.frame_text(
            self.__installed_text_frame,
            "",
            font_size=16,
        )
        self.__installed_text.pack()

    def __setup_ui_buttons(self):
        self.__btns_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        self.__install_btn = self.__ui_button(
            self.__btns_frame, "Install", self.__install
        )
        self.__uninstall_btn = self.__ui_button(
            self.__btns_frame, "Uninstall", self.__uninstall
        )
        self.__delete_btn = self.__ui_button(self.__btns_frame, "Delete", self.__remove)
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
            fg_color=palette.BUTTON_BACKGROUND,
            text_color=palette.TEXT_COLOR_DARK,
            hover_color=palette.DIM_BEIGE,
        )
        btn.pack(padx=4)
        return btn

    def __reset_buttons(self):
        self.__install_btn.configure(text="Install", state="normal")
        self.__uninstall_btn.configure(text="Uninstall", state="normal")
        self.__delete_btn.configure(text="Delete", state="normal")

    def __install(self):
        self.__install_btn.configure(text="Installing...", state="disabled")
        with contextlib.suppress(BadZipFile):
            self.__mod.install()
        self.__install_btn.configure(text="Installed", state="normal")
        self.__installed_text.configure(text="Is installed: Yes")

    def __uninstall(self):
        self.__uninstall_btn.configure(text="Uninstalling...", state="disabled")
        self.__mod.uninstall()
        self.__uninstall_btn.configure(text="Uninstalled", state="normal")
        self.__installed_text.configure(text="Is installed: No")

    def __remove(self):
        self.__delete_btn.configure(text="Deleting...", state="disabled")
        self.__mod.delete()
        self.__delete_btn.configure(text="Deleted", state="disabled")
        self.__installed_text.configure(text="Is installed: Deleted")
        self.__page_change("DownloadedModsPage")
