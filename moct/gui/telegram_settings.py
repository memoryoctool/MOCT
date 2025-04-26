import webbrowser
from tkinter import *

from moct.config import Config
from moct.gui.icon import Icon
from moct.notifyer import Notifier


class TelegramSettingsGui:
    root = None

    @classmethod
    def window(cls):
        cls.root = cls.get_main_window()
        cls.get_header_block(cls.root)
        cls.get_token_block(cls.root)
        cls.get_chat_id_block(cls.root)
        cls.get_buttons_block(cls.root)
        return cls.root

    @classmethod
    def get_main_window(cls):
        pos = ''
        last_window_x = Config.get_param('gui', 'tg_settings', 'x', throw=False)
        last_window_y = Config.get_param('gui', 'tg_settings', 'y', throw=False)
        if last_window_x and last_window_y:
            pos = f'+{last_window_x}+{last_window_y}'

        root = Toplevel()
        root.iconphoto(True, Icon.get_as_file())
        root.title('MOCT - Telegram Settings')
        root.geometry(f'380x165{pos}')
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", lambda: cls.dismiss())
        root.grab_set()
        return root

    @classmethod
    def dismiss(cls):
        geometry = cls.root.geometry()
        position = geometry.split('+')
        if len(position) >= 3:
            x = int(position[1])
            y = int(position[2])

            Config.set_param(x, 'gui', 'tg_settings', 'x')
            Config.set_param(y, 'gui', 'tg_settings', 'y')

        cls.root.grab_release()
        cls.root.destroy()

    @classmethod
    def get_header_block(cls, root):
        Label(root, text="Enter your Telegram details to enable notifications (this is optional)").place(x=10, y=10)

    @classmethod
    def get_token_block(cls, root):
        Label(root, text="Telegram Bot Token:").place(x=10, y=50)
        cls.token_entry = Entry(root)
        cls.token_entry.insert(0, Config.get_telegram_bot_token())
        cls.token_entry.place(width=215, height=20, x=150, y=52)

    @classmethod
    def get_chat_id_block(cls, root):
        Label(root, text="Telegram Chat ID:").place(x=10, y=90)
        cls.chat_id_entry = Entry(root)
        cls.chat_id_entry.insert(0, Config.get_telegram_chat_id())
        cls.chat_id_entry.place(width=215, height=20, x=150, y=92)

    @classmethod
    def get_buttons_block(cls, root):
        Button(root, text="Test", command=cls.test_clicked).place(width=80, height=24, x=10, y=130)
        Button(root, text="Ok", command=cls.ok_clicked).place(width=80, height=24, x=110, y=130)
        link = Label(root, text="Need Help?", fg="blue", cursor="hand2")
        link.place(x=300, y=132)
        link.bind("<Button-1>",
                  lambda e: webbrowser.open_new("https://github.com/memoryoctool/MOCT/wiki/Integration-with-Telegream"))

    @classmethod
    def test_clicked(cls):
        Notifier.worker_queue.append([Notifier.send_test_message, [cls.token_entry.get(), cls.chat_id_entry.get()]])

    @classmethod
    def ok_clicked(cls):
        from moct.gui.main import MainGui
        Config.set_telegram_bot_token(cls.token_entry.get())
        Config.set_telegram_chat_id(cls.chat_id_entry.get())
        Notifier.update_bot_instance()
        MainGui.update_telegram_status_entry()
        cls.dismiss()
