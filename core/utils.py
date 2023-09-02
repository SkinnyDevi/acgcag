import customtkinter as ctk


def set_screen_geometry(root: ctk.CTk):
    size = get_screen_center(root)

    width, height = size[0] // 2, size[1] // 2
    anchors = width // 2, height // 2

    root.geometry(f"{width}x{height}+{anchors[0]}+{anchors[1]}")


def get_screen_center(root: ctk.CTk):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    return (screen_width, screen_height)
