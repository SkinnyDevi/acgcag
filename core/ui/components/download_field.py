import customtkinter as ctk
from typing import Callable

import core.ui.palette as palette
import core.ui.components.helpers as ui_helpers


class DownloadField(ctk.CTkFrame):
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
