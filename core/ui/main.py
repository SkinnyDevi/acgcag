import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components as components


def mount_ui(main_frame: ctk.CTk):
    """
    Mounts the UI declared here.
    """

    title_frame = ctk.CTkFrame(main_frame)
    title = components.frame_text(
        title_frame,
        "A Certain GUI for a Certain Anime Game",
        20,
        color=palette.BRIGHT_BEIGE,
    )
    title.pack()
    title_frame.pack(pady=15, padx=10, side=ctk.TOP, anchor="w")

    app_tabs = ctk.CTkTabview(
        main_frame,
        segmented_button_fg_color=palette.MAIN_GRAY,
        segmented_button_selected_color=palette.BRIGHT_BEIGE,
        segmented_button_selected_hover_color=palette.DIM_BEIGE,
        segmented_button_unselected_color=palette.DIM_BEIGE,
        segmented_button_unselected_hover_color=palette.BRIGHT_BEIGE,
        text_color=palette.WHITE,
    )
    app_tabs._segmented_button.configure(font=palette.APP_FONT(16))

    downloaded_tab = app_tabs.add("Downloaded Mods")
    import_tab = app_tabs.add("Import Mods")

    app_tabs.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)
