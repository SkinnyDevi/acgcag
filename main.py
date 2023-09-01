import tkinter as tk

import core.ui.palette as palette
import core.utils as utils
from core.ui.main import mount_ui


root = tk.Tk()
palette.setup_font()

root.wm_title("ACGCAG")
utils.set_screen_geometry(root)

main_frame = tk.Frame(bg=palette.MAIN_GRAY)
mount_ui(main_frame)
main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


if __name__ == "__main__":
    root.mainloop()
