from ..base import NBase


class NXApplication(NBase):
    from Xwt import Application

    _type = Application

    def __init__(self, platform=None):
        self._ = self._type
        self.initialize(platform=platform)

    def initialize(self, platform=None):
        from Xwt import ToolkitType
        if platform:
            if platform == "Wpf":
                _ = ToolkitType.Wpf
        else:
            import sys
            if sys.platform == "win32":
                _ = ToolkitType.Wpf
        self._.Initialize(_)

    def run(self):
        self._.Run()
