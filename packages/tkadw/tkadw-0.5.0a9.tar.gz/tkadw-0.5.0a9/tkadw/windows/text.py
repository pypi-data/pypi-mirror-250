from .drawwidget import AdwDrawWidget


class AdwText(AdwDrawWidget):
    id = "text"

    def __init__(self,
                 *args,
                 text: str = "",
                 radius: int = 14,
                 font=None,
                 width=150,
                 height=80,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.attr(
            back="#ffffff",
            back_focus="#ffffff",
            border="#e6e6e6",
            border_focus="#ebebeb",
            border_width=1,
            border_width_focus=1,
            bottomsheet="#9c9c9c",
            bottomsheet_focus="#005fb8",
            bottomsheet_width=1,
            bottomsheet_width_focus=2,
            font=font,
            radius=radius,
            text=text,
            text_default="#18191c",
            text_focus="#18191c",
        )

        self._init()

        self.default_palette()

    def _init(self):
        from tkinter import StringVar, Text

        if self._font is None:
            from tkinter.font import nametofont
            font = nametofont("TkDefaultFont")
        else:
            font = self._font

        self.element_widget_text_var = StringVar(value=self._text)
        self.element_widget_text = Text(self, borderwidth=0, insertwidth=1, font=font)

        # 绘制框架
        self.element_frame = self.roundrect2_draw(
            x1=self._border_width, y1=self._border_width,
            x2=self.winfo_width() - self._border_width,
            y2=self.winfo_height() - self._border_width,
            fill=self._back, outline=self._border, radius=self._radius,
            width=self._border_width,
        )

        self.element_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self._radius - self._border_width,
            height=self.winfo_height() - self._border_width * 2 - 5,
            window=self.element_widget_text
        )

        self.element_text_bottomsheet = self.create_rectangle(
            self._border_width + self._radius / 3,
            self.winfo_height() - self._border_width + self._radius,
            self.winfo_width() - self._border_width - self._radius / 3,
            self.winfo_height() - self._border_width,
            fill=self._bottomsheet, outline=self._bottomsheet,
            width=self._bottomsheet_width
        )

    def _draw(self, event=None):
        super()._draw(event)

        if self._is_focus:
            __back = self._back_focus
            __border = self._border_focus
            __border_width = self._border_width_focus
            __bottomsheet = self._bottomsheet_focus
            __bottomsheet_width = self._bottomsheet_width_focus
            __text = self._text_focus
        else:
            __back = self._back
            __border = self._border
            __border_width = self._border_width
            __bottomsheet = self._bottomsheet
            __bottomsheet_width = self._bottomsheet_width
            __text = self._text_default

        try:

            # 输入框组件

            self.element_widget_text.configure(
                background=__back, foreground=__text, selectforeground=__text,
                insertbackground=__text
            )

            self.coords(
                self.element_text,
                self.winfo_width() / 2, self.winfo_height() / 2,
            )

            self.itemconfigure(
                self.element_text,
                width=self.winfo_width() - self._radius - __border_width,
                height=self.winfo_height() - __border_width * 2 - 5,
            )

            # 边框

            self.roundrect2_redraw(
                self.element_frame,
                x1=self._border_width, y1=self._border_width,
                x2=self.winfo_width() - self._border_width,
                y2=self.winfo_height() - self._border_width,
                radius=self._radius,
            )

            self.itemconfigure(
                self.element_frame,
                fill=__back, outline=__border,
                width=__border_width,
            )

            # 底部样式

            if __bottomsheet_width <= 0:
                self.itemconfigure(
                    self.element_text_bottomsheet,
                    state="hidden"
                )
            else:
                self.itemconfigure(
                    self.element_text_bottomsheet,
                    state="normal"
                )

            self.coords(
                self.element_text_bottomsheet,
                __border_width + self._radius / 3,
                self.winfo_height() - __border_width + self._radius,
                self.winfo_width() - __border_width - self._radius / 3,
                self.winfo_height() - __border_width,
            )

            self.itemconfigure(
                self.element_text_bottomsheet,
                fill=__bottomsheet, outline=__bottomsheet,
                width=__bottomsheet_width
            )

        except AttributeError:
            pass

    def _event_focus_in(self, event=None):
        super()._event_focus_in()
        self.element_widget_text.focus_set()

    def default_palette(self):
        pass

    def palette(self, palette: dict):
        if self.id in palette:
            if "radius" in palette[self.id]:
                self._radius = palette[self.id]["radius"]
            if "default" in palette[self.id]:
                if "back" in palette[self.id]["default"]:
                    self._back = palette[self.id]["default"]["back"]
                if "border" in palette[self.id]["default"]:
                    self._border = palette[self.id]["default"]["border"]
                if "border_width" in palette[self.id]["default"]:
                    self._border_width = palette[self.id]["default"]["border_width"]
                if "bottomsheet" in palette[self.id]["default"]:
                    self._bottomsheet = palette[self.id]["default"]["bottomsheet"]
                if "bottomsheet_width" in palette[self.id]["default"]:
                    self._bottomsheet_width = palette[self.id]["default"]["bottomsheet_width"]
                if "fore" in palette[self.id]["default"]:
                    self._text_default = palette[self.id]["default"]["fore"]
            if "focus" in palette[self.id]:
                if "back" in palette[self.id]["focus"]:
                    self._back_focus = palette[self.id]["focus"]["back"]
                if "border" in palette[self.id]["focus"]:
                    self._border_focus = palette[self.id]["focus"]["border"]
                if "border_width" in palette[self.id]["focus"]:
                    self._border_width_focus = palette[self.id]["focus"]["border_width"]
                if "bottomsheet" in palette[self.id]["focus"]:
                    self._bottomsheet_focus = palette[self.id]["focus"]["bottomsheet"]
                if "bottomsheet_width" in palette[self.id]["focus"]:
                    self._bottomsheet_width_focus = palette[self.id]["focus"]["bottomsheet_width"]
                if "fore" in palette[self.id]["focus"]:
                    self._text_focus = palette[self.id]["focus"]["fore"]
        self.update()
