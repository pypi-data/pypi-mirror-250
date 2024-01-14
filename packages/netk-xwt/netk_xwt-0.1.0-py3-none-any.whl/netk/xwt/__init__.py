from .libs import (
    libs,
                   )
from ..core import NImport

xwt = NImport(libs["Xwt.dll"])

from .application import NXApplication
from .run import run_wpf
from .window import NXWindow
