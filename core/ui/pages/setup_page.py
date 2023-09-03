import requests
import threading
import sys
import customtkinter as ctk
from typing import Callable
from zipfile import ZipFile
from pathlib import Path

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers
from core.ui.components.custom_frame import ManagerPageFrame
from core.config.config_manager import ConfigManager


class _DownloadField(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        root: ctk.CTk,
        download_title: str,
        download_fn: Callable,
        raw_title=False,
    ):
        self.root = root
        self.raw_title = raw_title
        self.download_title = download_title
        self.download_fn = download_fn

        super().__init__(parent, fg_color=palette.MAIN_GRAY)

        self.__title_frame()
        self.__progress_frame()

    def __title_frame(self):
        """
        The download's title.
        """

        title = (
            self.download_title if self.raw_title else f"Download {self.download_title}"
        )
        _, self.title = ui_helpers.label_left_aligned(self, title, 16)

    def __progress_frame(self):
        """
        The download's progress bar.
        """

        progress_frame = ui_helpers.frame_left_aligned(self)
        self.progress_bar = ctk.CTkProgressBar(progress_frame, 500, 10)
        self.progress_bar.pack()
        self.progress_bar.set(0)

    def exec_download(self):
        """
        Start the download.
        """

        title = (
            self.download_title
            if self.raw_title
            else f"Downloading {self.download_title}"
        )
        self.title.configure(text=title)
        self.download_fn()

    def update_progress(self, value: int):
        """
        Updates the progress bar.
        """

        self.progress_bar.set(value)
        self.root.update_idletasks()

    def complete(self):
        """
        Marks the download field as complete.
        """
        self.update_progress(1)
        self.progress_bar.forget()

        title = (
            f"{self.download_title} - Completed"
            if self.raw_title
            else f"Download {self.download_title} - Completed"
        )
        self.title.configure(text=title)


class SetupPage(ManagerPageFrame):
    def __init__(self, parent: ctk.CTkFrame, root: ctk.CTk):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        ui_helpers.frame_text(
            self, "PROGRAM SETUP INSTALLER", 19, color=palette.BRIGHT_BEIGE
        ).pack(pady=30)
        self.page_pack()

        self.__setup_semaphore = threading.Semaphore()

        self.__start_setup_frame()
        self.__setup_downloads(root)
        self.__setup_processes(root)
        self.__finish_setup_frame()

    def page_pack(self):
        self.pack(fill=ctk.BOTH, padx=10, pady=10)

    def page_forget(self):
        self.forget()

    def __setup_downloads(self, root: ctk.CTk):
        """
        Instantiate the respective setup downloads.
        """

        self.__downloads: dict[str, _DownloadField] = {}

        self.__downloads["gimi"] = _DownloadField(
            self, root, "GIMI", self.__download_gimi
        )

    def __setup_processes(self, root: ctk.CTk):
        """
        Instantiate the respective setup processes.
        """

        self.__processes: dict[str, _DownloadField] = {}

        self.__processes["unzip_gimi"] = _DownloadField(
            self, root, "Extract GIMI", self.__extract_gimi, raw_title=True
        )
        self.__processes["create_mods_folder"] = _DownloadField(
            self,
            root,
            "Create mods folder",
            self.__create_custom_mods_folder,
            raw_title=True,
        )

    def __start_setup_frame(self):
        """
        Start setup button frame.
        """

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
        """
        Finish setup button frame.
        """

        self.finish_frame = ctk.CTkFrame(self, fg_color=palette.MAIN_GRAY)
        ui_helpers.frame_text(
            self.finish_frame,
            "Please open again the program after pressing 'Finish Setup'.",
            font_size=18,
        ).pack()
        ui_helpers.frame_text(
            self.finish_frame,
            "This only occurs on first program setup or if necessary files are missing.",
            font_size=18,
        ).pack()

        finish_setup_btn = ctk.CTkButton(
            self.finish_frame,
            text="Finish Setup",
            command=self.__change_to_mainapp,
            font=palette.APP_FONT(14),
        )
        finish_setup_btn.pack(pady=20)

    def __start_setup(self):
        """
        Starts the setup (downloading, processing).
        """

        self.start_frame.forget()
        threading.Thread(target=self.__initiate_downloads).start()
        threading.Thread(target=self.__initiate_local_setup).start()

    def __initiate_downloads(self):
        """
        Locks the threads and downloads all instantiated downloads.
        """

        self.__setup_semaphore.acquire()
        for download in self.__downloads.values():
            download.exec_download()
        self.__setup_semaphore.release()

    def __initiate_local_setup(self):
        """
        Locks the threads and processes all instantiated processes.
        """

        self.__setup_semaphore.acquire()
        for proc in self.__processes.values():
            proc.exec_download()
        self.__setup_semaphore.release()
        self.__on_finish_setup()

    def __on_finish_setup(self):
        """
        Cleanup to do when setup is finished.
        """

        self.finish_frame.pack(pady=20, fill=ctk.BOTH, expand=True)
        config = ConfigManager.setup()
        config.completed_setup()

    def __change_to_mainapp(self):
        """
        Change the app to the main manager.
        """

        sys.exit(0)

    def __gimi_exists(self):
        """
        Verifies GIMI exists.
        """

        return Path("3dmigoto").exists()

    def __initialize_field(self, name: str, is_download=True):
        """
        Initializes a download or process field, waiting for it's visibility on screen.
        """

        handler = self.__downloads if is_download else self.__processes
        proc = handler[name]
        proc.pack()
        proc.wait_visibility()

        return proc

    def __download_gimi(self):
        """
        Downloads GIMI from GitHub.
        """

        gimi_download = self.__initialize_field("gimi")

        if self.__gimi_exists():
            gimi_download.complete()
            return

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

    def __extract_gimi(self):
        """
        Unzips the downloaded 3dmigoto file.
        """

        unzip_proc = self.__initialize_field("unzip_gimi", False)

        if self.__gimi_exists():
            unzip_proc.complete()
            return

        path = Path("3dmigoto-GIMI-for-playing-mods.zip")

        with ZipFile(path, "r") as zip_file:
            zip_file.extractall(".")

        path.unlink()

        custom_mod_folder = Path("acgcag_mods")
        if not custom_mod_folder.exists():
            custom_mod_folder.mkdir()

        unzip_proc.complete()

    def __create_custom_mods_folder(self):
        """
        Creates the manager's custom mod folder.
        """
        proc = self.__initialize_field("create_mods_folder", False)

        custom_mod_folder = Path("acgcag_mods")
        if not custom_mod_folder.exists():
            custom_mod_folder.mkdir()

        proc.complete()
