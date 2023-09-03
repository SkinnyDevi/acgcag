import customtkinter as ctk

import core.ui.palette as palette
import core.ui.components as components


class ModManagerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=palette.MAIN_GRAY)
        components.frame_text(self, "MOD MANAGER", 16).pack()
        self.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)

        app_tabs = ctk.CTkTabview(
            self,
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
