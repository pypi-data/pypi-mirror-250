from tkinter import Tk


class AdwRun(object):
    def __init__(self, root: Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def run(self):
        self.q = False
        while not self.q:
            self.root.update()

    def quit(self):
        self.q = True
        self.root.quit()


def run(root):
    AdwRun(root).run()


class Adw(Tk):
    def __init__(self, *args, master=None, title: str = "adw", config: bool = False,
                 dark: bool = True, dark_with_refresh: bool = False,
                 wincaption=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)

        if config:
            self.appconfig()

        self.default_palette()

        self.windark = dark

        try:
            try:  # >= win 8.1
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except:  # win 8.0 or less
                ctypes.windll.user32.SetProcessDPIAware()

            # ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            self.call('tk', 'scaling', ScaleFactor / 75)
        except:
            pass
        self.style_dark_with_icon(dark, dark_with_refresh)

        from sys import platform
        if platform == "win32" and wincaption is not None:
            from pywinstyles import change_header_color
            change_header_color(self, wincaption)
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def animation(self):
        from threading import Thread

        def start():
            print("Start")
            alpha = 0
            from time import sleep
            sleep(0.5)
            for frame in range(25):
                try:
                    alpha += 4
                    self.attributes("-alpha", (frame + 1) / 200 + (alpha) / 100)
                    print(self.attributes("-alpha"))
                    sleep(0.001)
                    self.update()
                except RuntimeError:
                    break

        t = Thread(target=lambda: start())
        self.after(100, lambda: t.start())

    def appconfig(self):
        from tkadw4.utility.appconfig import appconfig
        appconfig()

    def bind_move(self, widget):
        def _click(event):
            global x, y
            x, y = event.x, event.y

        def _move(event):
            new_x = (event.x - x) + self.winfo_x()
            new_y = (event.y - y) + self.winfo_y()
            s = f"+{new_x}+{new_y}"
            self.geometry(s)

        widget.bind("<Button-1>", _click, add="+")
        widget.bind("<B1-Motion>", _move, add="+")

    def custom(self, tcolor="#0a080a"):
        from tkadw4.windows.theme import AdwTFrame
        self.overrideredirect(True)

        from sys import platform

        self.frame = AdwTFrame()
        self.frame.pack(fill="both", expand="yes")
        self.frame.configure(background=tcolor)

        if platform == "win32":
            self.attributes("-transparentcolor", tcolor)
        else:
            self.frame.frame_radius = 0
            self.frame.update()

        self.wm_attributes("-topmost", True)

    def default_palette(self):
        pass

    def icon_dark(self, enable: bool):
        from tempfile import mkstemp

        _adwite_light = b"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"
        _adwite_dark = b"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"

        _, _adwite_light_temp = mkstemp()
        _, _adwite_dark_temp = mkstemp()

        with open(_adwite_light_temp, "wb") as _adwite_light_file:
            from base64 import b64decode
            _adwite_light_file.write(b64decode(_adwite_light))

        with open(_adwite_dark_temp, "wb") as _adwite_dark_file:
            from base64 import b64decode
            _adwite_dark_file.write(b64decode(_adwite_dark))

        adwite_light_icon = (_adwite_light_temp).replace("\\", "//")
        adwite_dark_icon = (_adwite_dark_temp).replace("\\", "//")

        def adwite_light_photo():
            from tkinter import PhotoImage
            return PhotoImage(file=adwite_light_icon)

        def adwite_dark_photo():
            from tkinter import PhotoImage
            return PhotoImage(file=adwite_dark_icon)

        try:
            if enable:
                icon = adwite_dark_photo()
            else:
                icon = adwite_light_photo()
            try:
                self.iconphoto(False, icon)
            except:
                pass
        except:
            pass

    def palette(self, dict):
        if dict is not None:
            if "window" in dict:
                self.configure(background=dict["window"]["back"])

    def quit(self):
        self.q = True
        super().quit()

    def run(self):
        self.q = False
        while not self.q:
            self.update()

    def style(self, stylename):
        """
        Windows平台下修改窗口样式

        Args:
            stylename (str): ["dark", "mica", "aero", "transparent", "acrylic", "win7",
                  "inverse", "popup", "native", "optimised", "light"], 参见https://github.com/Akascape/py-window-styles?tab=readme-ov-file#window-stylesthemes

        """
        from pywinstyles import apply_style
        apply_style(self, stylename)

    def style_dark(self, enable: bool, dark_with_refresh: bool = False):
        from sys import platform
        from os import system
        from customtkinter import set_appearance_mode
        if platform == "win32":
            if enable:
                from pywinstyles import apply_style
                apply_style(self, "dark")
            else:
                from pywinstyles import apply_style
                apply_style(self, "light")
            if dark_with_refresh:
                self.withdraw()
                self.iconify()
                self.focus_set()
        if platform == "darwin":
            if enable:
                system("defaults write -g NSRequiresAquaSystemAppearance -bool No")
            else:
                system("defaults delete -g NSRequiresAquaSystemAppearance")

    def style_dark_with_icon(self, enable: bool, dark_with_refresh: bool = False):
        try:
            self.style_dark(enable, dark_with_refresh)
            self.icon_dark(enable)
        except ModuleNotFoundError:
            pass

    def style_border(self, color):
        from pywinstyles import change_border_color
        change_border_color(self, color)

    def style_title(self, color):
        from pywinstyles import change_title_color
        change_title_color(self, color)

    def style_header(self, color):
        from pywinstyles import change_header_color
        change_header_color(self, color)

    def titlebar(self, enable: bool):
        self.wm_overrideredirect(not enable)
