import customtkinter as ctk

from core.ui.app import MainApp

root = ctk.CTk()
app = MainApp(root)

if __name__ == "__main__":
    root.mainloop()
