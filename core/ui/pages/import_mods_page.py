import contextlib
import threading
import customtkinter as ctk

import core.utils as utils
import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers
from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.components.download_field import DownloadField
from core.services.gamebanana_api import GameBananaAPI, ModPost


class ImportModsPage(ManagerPageFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        self.__search_thread = None

        title = ui_helpers.frame_text(
            self, "IMPORT MODS FROM GAMEBANANA", 20, color=palette.BRIGHT_BEIGE
        )
        title.pack(pady=10)

        container = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        container.pack()

        self.__entry_label(container)
        self.__entry_frame(container)
        self.__search_btn_frame(container)
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

    def __search_btn_frame(self, frame: ctk.CTkFrame):
        search_mod_frame = ui_helpers.frame_left_aligned(frame)
        self.__search_btn = ctk.CTkButton(
            search_mod_frame,
            text="Search",
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
            text_color=palette.WHITE,
            font=palette.APP_FONT(16),
            command=self.__start_search,
        )
        self.__search_btn.pack()
        self.__search_btn.bind("<Button-1>", lambda x: self.focus())

    def __mod_info(self):
        self.__mod_info_frame = UIModInfoFrame(self)
        self.__download_opts_frame = UIDownloadOptionsFrame(self)

    def __start_search(self):
        if self.__search_thread:
            return

        self.__search_thread = threading.Thread(target=self.__search)
        self.__search_thread.start()

    def __prepare_search(self):
        self.__mod_info_frame.page_forget()
        self.__download_opts_frame.page_forget()
        self.__search_btn.configure(state="disabled", text="Loading...")

    def __search(self):
        self.__prepare_search()

        url = self.__entry.get().strip()
        if url == "":
            return self.__search_cleanup()

        try:
            mod = GameBananaAPI.mod_from_url(url)
        except Exception:
            return self.__search_cleanup()

        self.__mod_info_frame.set_mod(mod, self.__download_opts_frame)
        self.__mod_info_frame.page_pack()

        self.__search_cleanup()

    def __search_cleanup(self):
        self.__search_thread = None
        self.__search_btn.configure(state="normal", text="Search")


class UIDownloadOptionsFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        ui_helpers.frame_text(self, "Available Downloads", 16).pack()
        self.__finish()

        self.__fields: list[ctk.CTkFrame] = []

    def page_pack(self):
        self.__finish_btn.pack()
        self.pack(pady=10)

    def page_forget(self):
        self.forget()
        self.__finish_btn.forget()
        with contextlib.suppress(Exception):
            self.destroy_frames()

    def set_mod(self, mod: ModPost):
        def pairwise(iterable):
            "s -> (s0, s1), (s2, s3), (s4, s5), ..."
            a = iter(iterable)
            return zip(a, a)

        downloads = mod.downloads
        for dl1, dl2 in pairwise(downloads):
            frame = self.__pack_download(dl1, dl2)
            self.__fields.append(frame)

        odd_dls = len(downloads) % 2 != 0
        if odd_dls:
            frame = self.__pack_download(downloads[-1])
            self.__fields.append(frame)

    def destroy_frames(self):
        for f in self.__fields:
            f.destroy()

        self.__fields.clear()

    def __pack_download(self, dl1: ModPost.Download, dl2: ModPost.Download = None):
        frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        frame.pack()

        self.__individual_download(frame, dl1)

        if dl2 is not None:
            self.__individual_download(frame, dl2)

        return frame

    def __individual_download(self, parent: ctk.CTkFrame, dl: ModPost.Download):
        frame = ui_helpers.frame_left_aligned(parent, fg_color=palette.MAIN_GRAY)

        title = (
            f"{dl.file_name[:25]}..."
            if len(dl.file_name.strip()) > 25
            else dl.file_name.strip()
        )
        ui_helpers.label_left_aligned(frame, title, 16)
        download_btn = ctk.CTkButton(
            frame,
            text="Download",
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
            text_color=palette.WHITE,
            font=palette.APP_FONT(16),
            command=lambda: print("Download", dl.file_name),
        )
        download_btn.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")

    def __finish(self):
        self.__finish_btn = ctk.CTkButton(
            self,
            text="Clear Search",
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
            text_color=palette.WHITE,
            font=palette.APP_FONT(16),
            command=self.page_forget,
        )


class UIModInfoFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        image_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        image_frame.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")

        info_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        info_frame.pack(pady=15, padx=10, side=ctk.RIGHT, anchor="e")

        self.__text_info(info_frame)
        self.__download_btn_frame(info_frame)

        self.__preview_label = ui_helpers.frame_text(image_frame, "Preview Image", 17)
        self.__mod_preview = ctk.CTkLabel(image_frame, text="", corner_radius=5)

    def page_pack(self):
        utils.pack_and_wait(self, pady=10)
        utils.pack_and_wait(self.__preview_label)
        utils.pack_and_wait(self.__mod_preview, expand=True, fill=ctk.BOTH)

    def page_forget(self):
        self.forget()
        self.__preview_label.forget()
        self.__mod_preview.forget()

    def __text_info(self, info_frame: ctk.CTkFrame):
        self.__name_text = "Name: "
        self.__id_text = "Mod Id: "
        self.__nsfw_text = "Is NSFW: "

        self.__mod_name = ui_helpers.frame_text(info_frame, self.__name_text, 17)
        self.__mod_name.pack(pady=5)
        self.__mod_id = ui_helpers.frame_text(info_frame, self.__id_text, 17)
        self.__mod_id.pack(pady=5)
        self.__mod_nsfw = ui_helpers.frame_text(info_frame, self.__nsfw_text, 17)
        self.__mod_nsfw.pack(pady=5)

    def __download_btn_frame(self, frame: ctk.CTkFrame):
        dl_frame = ctk.CTkFrame(frame, fg_color=palette.MAIN_GRAY)
        self.__search_btn = ctk.CTkButton(
            dl_frame,
            text="Download",
            fg_color=palette.BUTTON_BG_GRAY,
            hover_color=palette.DIM_BEIGE,
            text_color=palette.WHITE,
            font=palette.APP_FONT(16),
            command=self.__download,
        )
        self.__search_btn.pack()
        dl_frame.pack(pady=10)

    def set_mod(self, mod: ModPost, download_opts: UIDownloadOptionsFrame):
        self.__download_opts = download_opts
        self.__download_opts.set_mod(mod)

        self.__mod_name.configure(text=self.__name_text + mod.mod_name)
        self.__mod_id.configure(text=self.__id_text + mod.itemid)
        self.__mod_nsfw.configure(text=self.__nsfw_text + str(mod.nsfw))

        preview = mod.preview_image
        self.__preview_image = ctk.CTkImage(dark_image=preview, size=preview.size)
        self.__mod_preview.configure(image=self.__preview_image)

    def __download(self):
        self.page_forget()
        self.__download_opts.page_pack()
