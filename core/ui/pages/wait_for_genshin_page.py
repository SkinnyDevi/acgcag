import customtkinter as ctk
from PIL import Image
from pathlib import Path
from observable import Observable

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers
from core.ui.components.custom_frame import ManagerPageFrame


class WaitForGenshinPage(ManagerPageFrame):
    page_change_event = Observable()

    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        container = ctk.CTkFrame(
            self, fg_color=palette.MAIN_GRAY, width=1000, height=500
        )
        container.pack(ipady=100)
        container.propagate(False)
        ui_helpers.frame_text(
            container, "3DMIGOTO HAS LAUNCHED", 20, color=palette.BRIGHT_BEIGE
        ).pack(ipady=20)

        self.__mona_icon(container)
        self.__info(container)

    def page_pack(self):
        self.pack(pady=20, padx=20)

    def page_forget(self):
        self.forget()

    def __change_to_mods_page(self):
        WaitForGenshinPage.page_change_event.trigger(
            "page_change", "DownloadedModsPage"
        )

    def __mona_icon(self, frame: ctk.CTkFrame):
        icon_path = Path("assets/mona-love-icon.png")
        raw = Image.open(icon_path)
        img = ctk.CTkImage(dark_image=raw, size=(100, 100))
        icon_label = ctk.CTkLabel(frame, text="", image=img)
        icon_label.pack()

    def __info(self, container: ctk.CTkFrame):
        frame = ctk.CTkFrame(
            container,
            fg_color=palette.MENU_BACKGROUND,
            border_color=palette.DIM_BEIGE,
            border_width=2,
        )
        frame.pack(pady=30, ipadx=10)

        ui_helpers.frame_text(
            frame,
            "Please wait for 3DMigoto to finish loading!",
            20,
            color=palette.BRIGHT_BEIGE,
            background=palette.MENU_BACKGROUND,
        ).pack(pady=20)

        ui_helpers.frame_text(
            frame,
            "1. Open Genshin Impact",
            18,
            color=palette.BRIGHT_BEIGE,
            background=palette.MENU_BACKGROUND,
        ).pack(pady=5)
        ui_helpers.frame_text(
            frame,
            "2. Once the 3DMigoto window closes, you can press the button below",
            18,
            color=palette.BRIGHT_BEIGE,
            background=palette.MENU_BACKGROUND,
        ).pack(pady=5)

        ctk.CTkButton(
            frame,
            text="3DMigoto Finished Loading",
            fg_color=palette.BUTTON_BACKGROUND,
            hover_color=palette.DIM_BEIGE,
            text_color=palette.TEXT_COLOR_DARK,
            command=self.__change_to_mods_page,
            font=palette.APP_FONT(18),
        ).pack(pady=20)
