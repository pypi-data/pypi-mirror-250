from ..base import NBase


class NXWindow(NBase):
    from Xwt import Window

    _type = Window

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispose(self):
        self._.Dispose()

    def show(self):
        self._.Show()
