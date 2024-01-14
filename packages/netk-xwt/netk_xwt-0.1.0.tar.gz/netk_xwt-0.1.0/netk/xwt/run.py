from ..core import NImport

Winforms = NImport('System.Windows.Forms')
Threading = NImport('System.Threading')
from System import IntPtr, Int32, Func, Type, Environment
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart,SynchronizationContext,SendOrPostCallback


def run_wpf(main):
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
