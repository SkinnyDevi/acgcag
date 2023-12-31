import threading
import customtkinter as ctk
from observable import Observable

import core.utils as utils
import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers

from core.services.gamebanana_api import GameBananaAPI, ModPost
from core.ui.components.custom_frame import ManagerPageFrame
from core.ui.components.download_field import DownloadField


class ImportModsPage(ManagerPageFrame):
    search_btn_obs = Observable()

    def __init__(self, parent: ctk.CTkFrame, root: ctk.CTk):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        self.__search_thread = None
        self.app_root = root

        title = ui_helpers.frame_text(
            self, "IMPORT SKINS FROM GAMEBANANA", 20, color=palette.BRIGHT_BEIGE
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
            fg_color=palette.BUTTON_BACKGROUND,
            text_color=palette.TEXT_COLOR_DARK,
            font=palette.APP_FONT(15),
            placeholder_text="https://gamebanana.com/mods/465880",
        )
        self.__entry.pack()

    def __search_btn_frame(self, frame: ctk.CTkFrame):
        search_mod_frame = ui_helpers.frame_left_aligned(frame)
        self.__search_btn = ctk.CTkButton(
            search_mod_frame,
            text="Search",
            fg_color=palette.BUTTON_BACKGROUND,
            text_color=palette.TEXT_COLOR_DARK,
            hover_color=palette.DIM_BEIGE,
            font=palette.APP_FONT(16),
            command=self.__start_search,
        )
        self.__search_btn.pack()
        self.__search_btn.bind("<Button-1>", lambda x: self.focus())

        ImportModsPage.search_btn_obs.on(
            "state_change", lambda x: self.__search_btn_state(x)
        )

    def __search_btn_state(self, state: bool):
        change = "normal" if state else "disabled"
        self.__search_btn.configure(state=change)

    def __mod_info(self):
        self.__mod_info_frame = UIModInfoFrame(self)
        self.__download_opts_frame = UIDownloadOptionsFrame(self, self.app_root)

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
    def __init__(self, parent: ctk.CTkFrame, root: ctk.CTk):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        self.root = root
        self.__dl_bar: DownloadField = None

        ui_helpers.frame_text(self, "Available Downloads", 16).pack()

        self.__finish()

        self.__fields: list[ctk.CTkFrame] = []

    def page_pack(self):
        self.__finish_btn.pack(pady=5)
        self.pack(pady=10)

    def page_forget(self):
        self.destroy_frames()
        self.forget()
        self.__finish_btn.forget()
        self.__finish_btn.configure(text="Clear Search", command=self.page_forget)

    def set_mod(self, mod: ModPost):
        downloads = mod.downloads
        for dl1, dl2 in utils.pairwise(downloads):
            frame = self.__pack_download(dl1, dl2)
            self.__fields.append(frame)

    def destroy_frames(self):
        if self.__dl_bar is not None:
            self.__dl_bar.destroy()

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
            fg_color=palette.BUTTON_BACKGROUND,
            text_color=palette.TEXT_COLOR_DARK,
            hover_color=palette.DIM_BEIGE,
            font=palette.APP_FONT(16),
        )
        download_btn.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")
        download_btn.configure(command=lambda: self.__start_download(dl))

    def __start_download(self, download: ModPost.Download):
        thread = threading.Thread(target=self.__download_file, args=[download])
        thread.start()

    def __download_file(self, download: ModPost.Download):
        ImportModsPage.search_btn_obs.trigger("state_change", False)
        self.__dl_bar = DownloadField(
            self, self.root, download.file_name, download.download
        )
        download.dl_obs.on("mod_chunk_update", self.__dl_bar.update_progress)
        download.dl_obs.on("mod_dl_complete", lambda x: self.__dl_bar.complete())

        for f in self.__fields:
            f.forget()
        self.__finish_btn.forget()

        utils.pack_and_wait(self.__dl_bar)
        self.__dl_bar.exec_download()

        def finish():
            self.page_forget()
            self.__dl_bar.forget()

        self.__finish_btn.configure(text="Finish", command=finish)
        self.__finish_btn.pack(pady=5)
        ImportModsPage.search_btn_obs.trigger("state_change", True)

    def __finish(self):
        self.__finish_btn = ctk.CTkButton(
            self,
            text="Clear Search",
            fg_color=palette.BUTTON_BACKGROUND,
            text_color=palette.TEXT_COLOR_DARK,
            hover_color=palette.DIM_BEIGE,
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
        self.__id_text = "GB Id: "
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
            fg_color=palette.BUTTON_BACKGROUND,
            text_color=palette.TEXT_COLOR_DARK,
            hover_color=palette.DIM_BEIGE,
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
