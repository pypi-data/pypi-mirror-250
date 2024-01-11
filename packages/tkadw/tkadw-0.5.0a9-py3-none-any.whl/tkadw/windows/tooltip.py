from .window import AdwWindow


class AdwToolTip(AdwWindow):
    def __init__(self, master, *args, pady=5, text: str = "", **kwargs):
        super().__init__(*args, **kwargs)

        self.frameless(True)

        self.widget = master
        self.widget.bind("<Enter>", self._enter, add="+")
        self.widget.bind("<Leave>", self._leave, add="+")

        from .label import AdwLabel
        from .frame import AdwFrame

        self.border = AdwFrame(self, width=100, height=30)
        self.label = AdwLabel(self.border, text=text)
        self.label.pack()
        self.border.pack(fill="both", expand="yes")

        self.attr(
            pady=pady,
        )

        self.default_palette()

        self.withdraw()

    def _enter(self, event):
        self.deiconify()
        self.attributes("-topmost", True)
        self.geometry(
            f"+{round(self.widget.winfo_width() / 2 + self.widget.winfo_rootx() - self.winfo_width() / 2)}+{self.widget.winfo_rooty() + self.widget.winfo_height() + self._pady}")

    def _leave(self, event):
        self.withdraw()

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        super().palette(palette)
        try:
            self.label.palette(palette)
            self.border.palette(palette)
        except:
            pass
