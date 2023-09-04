import itertools
import customtkinter as ctk
from pathlib import Path
from typing import Iterable

__WIN_WIDTH = 1200
__WIN_HEIGHT = 600


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
