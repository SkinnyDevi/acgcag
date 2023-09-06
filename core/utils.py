import itertools
import customtkinter as ctk
from pathlib import Path
from typing import Iterable

__WIN_WIDTH = 1200
__WIN_HEIGHT = 599


def get_window_size():
    return __WIN_WIDTH, __WIN_HEIGHT


def set_screen_geometry(root: ctk.CTk):
    width, height = get_window_size()
    anchors = width // 2, height // 2

    root.geometry(f"{width+100}x{height+100}+{anchors[0]-65}+{anchors[1]-65}")


def directory_is_empty(directory: Path) -> bool:
    return not any(directory.iterdir())


def missing_files():
    gimi = Path("3dmigoto")
    custom_mods_folder = Path("acgcag_mods")

    if gimi.exists() and custom_mods_folder.exists():
        gimi_exists = not directory_is_empty(gimi) and gimi.is_dir()
        custom_mods_exists = custom_mods_folder.is_dir()

        return not (gimi_exists and custom_mods_exists)
    else:
        return True


def pack_and_wait(component: ctk.CTkBaseClass, **kwargs):
    component.pack(**kwargs)
    component.wait_visibility()


def pairwise(iterable: Iterable, fill=True):
    """
    Returns an iterable with paired values.

    By default, it fills odd iterables with `None`.
    """
    a = iter(iterable)

    if fill:
        filler = [None for _ in range(len(iterable) % 2)]
        a = itertools.chain(a, filler)

    return zip(a, a)


def triplets_of(iterable: Iterable, fill=True):
    """
    Returns an iterable with paired values.

    By default, it fills non-triplet iterables with `None`.
    """

    # triplet filler
    l = iter(iterable)
    if fill:
        to_fill = len(iterable) % 3
        if to_fill == 0:
            return zip(l, l, l)
        amount = 0 if to_fill == 3 else 3 - to_fill

        # triplet iterable
        l = itertools.chain(l, [None for _ in range(amount)])

    return zip(l, l, l)


import shutil
import contextlib
from zipfile import ZipFile
from pyunpack import Archive
from py7zr import SevenZipFile


class MultiExtensionExtractor:
    def __init__(self, file_path: Path, mod_id: str):
        self._file = file_path
        self._mod_id = mod_id

    def extract(self) -> Path:
        if not Path("3dmigoto").exists():
            raise FileNotFoundError(
                "3dmigoto was not found. Please re-open the app to re-run the setup process"
            )

        return self.__extension_parser()

    def __extension_parser(self):
        ext = self._file.suffix

        match ext:
            case ".zip":
                return self.__zip_extract()

            case ".7z":
                return self.__7z_extract()

            case ".rar":
                return self.__rar_extract()

    def __zip_extract(self):
        path = self.__extract_path()
        with ZipFile(self._file, "r") as mod_file:
            mod_file.extractall(path)

        return path

    def __7z_extract(self):
        path = self.__extract_path()
        file = SevenZipFile(self._file)
        file.extractall(path)
        return path

    def __rar_extract(self):
        path = self.__extract_path()

        file = Archive(self._file)
        file.extractall(path)
        return path

    def __extract_path(self):
        path = Path(f"3dmigoto/Mods/{self._mod_id}")

        if path.exists():
            with contextlib.suppress(Exception):
                for f in path.glob("*"):
                    shutil.rmtree(f)
        else:
            path.mkdir()

        return path
