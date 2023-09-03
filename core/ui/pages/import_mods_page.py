import customtkinter as ctk

import core.utils as utils
import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers
from core.ui.components.custom_frame import ManagerPageFrame
from core.services.gamebanana_api import GameBananaAPI, ModPost


class ImportModsPage(ManagerPageFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        title = ui_helpers.frame_text(
            self, "IMPORT MODS FROM GAMEBANANA", 20, color=palette.BRIGHT_BEIGE
        )
        title.pack(pady=10)

        container = ctk.CTkFrame(self)
        container.pack()

        self.__entry_label(container)
        self.__entry_frame(container)
        self.__search_btn(container)
        self.__mod_info()

        self.bind("<Button-1>", lambda x: self.focus())

    def page_pack(self):
        self.pack(pady=10)

    def page_forget(self):
        self.forget()

    def __entry_label(self, frame: ctk.CTkFrame):
        ui_helpers.label_left_aligned(frame, "GameBanana Mod URL:", font_size=16)

    def __entry_frame(self, frame: ctk.CTkFrame):
        entry_frame = ui_helpers.frame_left_aligned(frame)
        self.__entry = ctk.CTkEntry(
            entry_frame,
            width=325,
            height=32,
            font=palette.APP_FONT(15),
            placeholder_text="https://gamebanana.com/mods/465880",
        )
        self.__entry.pack()

    def __search_btn(self, frame: ctk.CTkFrame):
        search_mod_frame = ui_helpers.frame_left_aligned(frame)
        search_btn = ctk.CTkButton(
            search_mod_frame,
            text="Search",
            fg_color=palette.BUTTON_BG_GRAY,
            text_color=palette.WHITE,
            font=palette.APP_FONT(16),
            command=self.__search,
        )
        search_btn.pack()
        search_btn.bind("<Button-1>", lambda x: self.focus())

    def __mod_info(self):
        self.__mod_info_frame = UIModInfoFrame(self)

    def __search(self):
        self.__mod_info_frame.page_forget()

        url = self.__entry.get().strip()
        if url == "":
            return

        mod = GameBananaAPI.mod_from_url(url)
        self.__mod_info_frame.set_mod(mod)
        self.__mod_info_frame.page_pack()


class UIModInfoFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent)

        self.__name_text = "Name: "
        self.__id_text = "Mod Id: "
        self.__nsfw_text = "Is NSFW: "

        _, self.__mod_name = ui_helpers.label_left_aligned(self, self.__name_text, 15)
        _, self.__mod_id = ui_helpers.label_left_aligned(self, self.__id_text, 15)
        _, self.__mod_nsfw = ui_helpers.label_left_aligned(self, self.__nsfw_text, 15)

        self.__preview_label = ui_helpers.frame_text(parent, "Preview Image", 15)
        self.__mod_preview = ctk.CTkLabel(parent, text="")

    def page_pack(self):
        utils.pack_and_wait(self, pady=20)
        utils.pack_and_wait(self.__preview_label)
        utils.pack_and_wait(self.__mod_preview, expand=True, fill=ctk.BOTH)

    def page_forget(self):
        self.forget()
        self.__preview_label.forget()
        self.__mod_preview.forget()

    def set_mod(self, mod: ModPost):
        self.__mod_name.configure(text=self.__name_text + mod.mod_name)
        self.__mod_id.configure(text=self.__id_text + mod.itemid)
        self.__mod_nsfw.configure(text=self.__nsfw_text + str(mod.nsfw))

        preview = mod.preview_image
        self.__preview_image = ctk.CTkImage(dark_image=preview, size=preview.size)
        self.__mod_preview.configure(image=self.__preview_image)
