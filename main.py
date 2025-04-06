import asyncio
import threading

from moct.config import Config
from moct.gui.main import MainGui
from moct.memtest import MemTest
from moct.notifyer import Notifier

VERSION = "1.0.4"


def main():
    # Setup
    root = MainGui.window()
    MemTest.do_test = Config.get_run_tests_on_startup()
    MainGui.update_run_tests_text()

    # Workers
    threading.Thread(target=Notifier.worker, daemon=True).start()
    threading.Thread(target=MemTest.worker, daemon=True).start()

    # Main thread
    root.mainloop()

    try:
        asyncio.run(Notifier.bot().session.close())
    except:
        pass


if __name__ == "__main__":
    main()
