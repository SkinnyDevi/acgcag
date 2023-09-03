import shutil
import customtkinter as ctk
from pathlib import Path


def get_screen_center(root: ctk.CTk):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    return (screen_width, screen_height)


def get_window_size(screen_width: int, screen_height: int):
    return screen_width // 2, screen_height // 2


def set_screen_geometry(root: ctk.CTk):
    screen_width, screen_height = get_screen_center(root)

    width, height = get_window_size(screen_width, screen_height)
    anchors = width // 2, height // 2

    root.geometry(f"{width}x{height}+{anchors[0]}+{anchors[1]}")


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
