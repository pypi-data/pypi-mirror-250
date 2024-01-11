from tkadw import *
from tkinter import *

theme = nametotheme(
    "ant"
)

window = AdwTMainWindow()
window.theme(theme, "dark")
window.geometry("540x380")

for widget in range(10):
    button = AdwTButton(window, text="AdwTButton", command=lambda: print("Button"))
    button.tooltip(button.id)
    button.pack(fill="x", padx=10, pady=10)

window.mainloop()
