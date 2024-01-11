class SysTray(object):
    def __init__(self, master=None, iconname=None, iconpath=None, callback=None, tooltip: str = None):
        from .root import root
        self.master = root(master)
        try:
            from tkwinico import Winico
        except ModuleNotFoundError:
            self.winico = None
        else:
            self.winico = Winico(self.master)
            self.icon = self.winico.icon(icon_name=iconname, icon_file=iconpath)
            self.winico.tray_add(self.icon, callback=callback, callback_args=("%message", "%i", "%x", "%y"), tooltip=tooltip)

    def destroy(self):
        self.winico.tray_delete(self.icon)
        self.winico.icon_delete(self.icon)