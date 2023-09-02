import customtkinter as ctk

import core.ui.palette as palette
import core.utils as utils
from core.ui.main import mount_ui


root = ctk.CTk()
palette.setup_font()

root.wm_title("ACGCAG")
utils.set_screen_geometry(root)

main_frame = ctk.CTkFrame(root, fg_color=palette.MAIN_GRAY)
mount_ui(main_frame)
main_frame.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=True)


if __name__ == "__main__":
    root.mainloop()
