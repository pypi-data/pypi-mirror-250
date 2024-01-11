from .layout import AdwLayout
from .base import AdwBase


class AdwWidget(AdwLayout, AdwBase):
    id = "widget"

    def tooltip(self, text: str = None):
        if text:
            if not hasattr(self, "_tooltip"):
                from .theme import AdwTToolTip
                self._tooltip = AdwTToolTip(self, text=text)
            self._tooltip.label.label_text(text)
        else:
            if hasattr(self, "_tooltip"):
                del self._tooltip
