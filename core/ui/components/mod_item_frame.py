import customtkinter as ctk
from typing import Callable

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers

from core.services.local_mod_manager import LocalMod
from core.ui.components.custom_frame import ManagerPageFrame


class ModItemFrame(ManagerPageFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        mod: LocalMod,
        on_manager: Callable = None,
        manage_button: bool = True,
        display_installed: bool = False,
    ):
        super().__init__(
            parent,
            width=365,
            height=215 if display_installed and manage_button else 180,
            border_width=2,
            border_color=palette.MAIN_BEIGE,
            fg_color=palette.VARIANT_GRAY,
        )
        self.propagate(False)
        self._mod = mod
        self._on_manager = on_manager
        self._manage_button = manage_button
        self._display_installed = display_installed

        self.__define_image()
        self.__define_info()

    def page_pack(self):
        self.pack(
            side=ctk.LEFT, fill=ctk.BOTH, expand=True, anchor="nw", padx=5, pady=5
        )

    def page_forget(self):
        self.forget()

    def update_installed_text(self):
        installed = f"Is installed: {'Yes' if self._mod.is_installed else 'No'}"
        self.__installed_text.configure(text=installed)

    def __define_image(self):
        image_frame = ctk.CTkFrame(
            self, fg_color=palette.MAIN_GRAY, width=110, height=110
        )
        image_frame.propagate(False)
        image_frame.pack(padx=10, pady=10, side=ctk.LEFT, anchor="w")

        i = self._mod.mod_preview_image
        img = ctk.CTkImage(dark_image=i, size=i.size)
        label = ctk.CTkLabel(image_frame, text="", image=img)
        label.pack()

    def __define_info(self):
        info_frame = ctk.CTkFrame(self, width=250, fg_color=palette.MAIN_GRAY)
        info_frame.propagate(False)
        info_frame.pack(padx=10, pady=10, side=ctk.RIGHT, anchor="e")

        self.__mod_label(info_frame, self._mod.name)
        self.__mod_label(info_frame, f"Id: {self._mod.itemid}")
        self.__mod_label(info_frame, f"NSFW: {self._mod.nsfw}")
        self.__mod_label(info_frame, f"Character: {self._mod.character}")

        if self._display_installed:
            self.__installed_text = self.__mod_label(
                info_frame,
                f"Is installed: {'Yes' if self._mod.is_installed else 'No'}",
            )

        if self._manage_button:
            btn = ctk.CTkButton(
                info_frame,
                text="Manage",
                font=palette.APP_FONT(14),
                fg_color=palette.BUTTON_BACKGROUND,
                text_color=palette.TEXT_COLOR_DARK,
                hover_color=palette.DIM_BEIGE,
                command=self._on_manager,
            )

            btn.pack(pady=5)

    def __mod_label(self, frame: ctk.CTkFrame, text: str):
        holder = ctk.CTkFrame(frame)
        holder.pack(pady=2, padx=4, side=ctk.TOP, anchor="nw")

        label = f"{text[:23]}..." if len(text.strip()) > 23 else text.strip()
        ctklabel = ui_helpers.frame_text(holder, label, 14)
        ctklabel.pack()

        return ctklabel
