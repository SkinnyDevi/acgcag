import requests
import threading
import asyncio
import customtkinter as ctk
from typing import Callable

import core.ui.palette as palette
import core.ui.components as components


class _DownloadField(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        root: ctk.CTk,
        download_title: str,
        download_fn: Callable,
    ):
        self.root = root
        self.download_title = download_title
        self.download_fn = download_fn

        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        title_frame = ctk.CTkFrame(self)
        self.title = components.frame_text(
            title_frame,
            f"Download {download_title}",
            16,
        )
        self.title.pack()
        title_frame.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")

        progress_frame = ctk.CTkFrame(self)
        self.progress_bar = ctk.CTkProgressBar(progress_frame, 500, 10)
        self.progress_bar.pack()
        self.progress_bar.set(0)
        progress_frame.pack(pady=15, padx=10, side=ctk.LEFT, anchor="w")

    def exec_download(self):
        self.title.configure(text=f"Downloading {self.download_title}")
        self.download_fn()

    def update_progress(self, value: int):
        self.progress_bar.set(value)
        self.root.update_idletasks()

    def complete(self):
        self.progress_bar.forget()
        self.title.configure(text=f"Download {self.download_title} - Completed")


class SetupPage(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, root: ctk.CTk):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        components.frame_text(self, "SETUP PAGE", 18).pack()
        self.pack(fill=ctk.BOTH, padx=10, pady=10)

        self.__setup_semaphore = threading.Semaphore()

        self.__start_setup_frame()
        self.__setup_downloads(root)
        self.__setup_processes(root)
        self.__finish_setup_frame()

    def __setup_downloads(self, root: ctk.CTk):
        self.__downloads: dict[str, _DownloadField] = {}

        self.__downloads["gimi"] = _DownloadField(
            self, root, "GIMI", self.__download_gimi
        )

    def __setup_processes(self, root: ctk.CTk):
        self.__processes: dict[str, _DownloadField] = {}

    def __start_setup_frame(self):
        self.start_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        start_setup_btn = ctk.CTkButton(
            self.start_frame,
            text="Start Setup",
            command=self.__start_setup,
            font=palette.APP_FONT(14),
        )
        start_setup_btn.pack()
        self.start_frame.pack(fill=ctk.BOTH, expand=True)

    def __finish_setup_frame(self):
        self.finish_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        finish_setup_btn = ctk.CTkButton(
            self.finish_frame,
            text="Finish Setup",
            command=self.__on_finish_setup,
            font=palette.APP_FONT(14),
        )
        finish_setup_btn.pack()

    def __start_setup(self):
        self.start_frame.forget()
        threading.Thread(target=self.__initiate_downloads).start()
        threading.Thread(target=self.__initiate_local_setup).start()

    def __initiate_downloads(self):
        self.__setup_semaphore.acquire()
        for download in self.__downloads.values():
            download.exec_download()
        self.__setup_semaphore.release()

    def __initiate_local_setup(self):
        self.__setup_semaphore.acquire()
        for proc in self.__processes.values():
            proc.exec_download()
        self.__setup_semaphore.release()
        self.__on_finish_setup()

    def __on_finish_setup(self):
        self.finish_frame.pack(fill=ctk.BOTH, expand=True)

    def __download_gimi(self):
        gimi_download = self.__downloads["gimi"]
        gimi_download.pack()
        gimi_download.wait_visibility()

        github_download_url = "https://github.com/SilentNightSound/GI-Model-Importer/releases/download/v7.0/3dmigoto-GIMI-for-playing-mods.zip"
        file_request = requests.get(github_download_url, stream=True)
        chunk_size = 10240
        file_size = int(file_request.headers["content-length"])

        with open("3dmigoto-GIMI-for-playing-mods.zip", "wb") as gimi:
            chunks = 0
            for chunk in file_request.iter_content(chunk_size):
                chunks += chunk_size
                gimi_download.update_progress(chunks / file_size)
                gimi.write(chunk)

        gimi_download.complete()
