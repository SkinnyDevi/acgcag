import tkinter as tk

window = tk.Tk()

window.wm_title("ACGCAG")


frame1 = tk.Frame(master=window, width=200, height=100, bg="#CCCCCC")
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

window.mainloop()
