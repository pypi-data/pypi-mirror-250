# 全是导入

from .base import AdwBase, Arg as AdwArgument
from .button import AdwButton
from .circularbutton import AdwCircularButton
from .closebutton import AdwCloseButton
from .customwindow import customwindow
from .dragarea import (
    WindowDragArea as AdwWindowDragArea,
    WidgetDragArea as AdwWidgetDragArea,
    bind_window_drag, bind_widget_drag,
    tag_bind_window_drag, tag_bind_widget_drag
)
from .drawengine import AdwDrawEngine
from .drawwidget import AdwDrawWidget
from .entry import AdwEntry
from .frame import AdwFrame
from .frame import AdwFrame as AdwPanel
from .gradient import (
    Gradient as AdwGradient, Gradient2 as AdwGradient2,
    ARC, CENTRAL, CIRCULAR, HORIZONTAL, VERTICAL,
    X, Y
)
from .icon import ICONLIGHT, ICONDARK
from .label import AdwLabel
from .layout import AdwLayout
from .manager import WindowManager as AdwWindowManager
from .mdi import AdwWindowsMDI  # 仅限Windows
from .menubar import AdwMenuBar, create_root_menubar
from .menubar import AdwMenuBar as AdwMenubar
from .roundrect import RoundRect as AdwRoundRect
from .run import AdwRun, run
from .separator import AdwSeparator
from .separator import AdwSeparator as AdwDivider
from .sizegrip import AdwSizegrip
from .style import WindowStyle as AdwWindowStyle, LIGHT, DARK
from .systray import SysTray as AdwWindowsSysTray  # 仅限Windows
from .text import AdwText
from .text import AdwText as AdwTextBox
from .theme import (
    AdwThemed, theme, theme_mode,
    AdwTButton, AdwTCircularButton, AdwTCloseButton, AdwTEntry,
    AdwTFrame, AdwTLabel, AdwTMainWindow, AdwTMenuBar,
    create_root_themed_menubar, AdwTSeparator, AdwTSizegrip,
    AdwTText, AdwTTitleBar, AdwTToolTip, AdwTWindow,
    AdwTWindowsMDI, set_default_theme
)
from .theme import (
    AdwTFrame as AdwTPanel,
    AdwTMenuBar as AdwTMenubar,
    AdwTSeparator as AdwTDivider,
    AdwTText as AdwTTextBox,
    AdwTTitleBar as AdwTTitlebar,
    AdwTToolTip as AdwBalloon
)
from .themes import *
from .tooltip import AdwToolTip
from .tooltip import AdwToolTip as AdwBalloon
from .titlebar import AdwTitleBar
from .widget import AdwWidget
from .window import AdwMainWindow, AdwWindow
