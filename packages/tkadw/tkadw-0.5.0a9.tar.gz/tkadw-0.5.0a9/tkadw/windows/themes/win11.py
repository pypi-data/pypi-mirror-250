from .theme import AdwTheme


class AdwWin11Theme(AdwTheme):

    path = "win11.json"

    def __init__(self, accent: list = None, system_accent_color=False):
        super().__init__()
        if accent:
            self.accent(accent[0], accent[1])
        else:
            try:
                from pywinstyles.py_win_style import get_accent_color
            except ModuleNotFoundError:
                pass
            else:
                if system_accent_color:
                    self.accent(get_accent_color(), get_accent_color())

    def accent(self, color, darkcolor):
        self.theme.light.entry.focus.bottomsheet = color
        self.theme.dark.entry.focus.bottomsheet = darkcolor
        self.theme.light.text.focus.bottomsheet = color
        self.theme.dark.text.focus.bottomsheet = darkcolor

