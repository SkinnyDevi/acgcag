import customtkinter as ctk


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
