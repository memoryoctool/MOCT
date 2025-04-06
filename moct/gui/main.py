import webbrowser
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from moct.config import Config
from moct.gui.about import AboutGui
from moct.gui.icon import Icon
from moct.gui.telegram_settings import TelegramSettingsGui
from moct.memtest import MemTest
from moct.notifyer import Notifier
from moct.windows import Windows


class MainGui:
    root = None
    logs = ''

    log_file = 'moct.log'

    @classmethod
    def window(cls):
        cls.root = cls.get_main_window()
        cls.get_menu_bar(cls.root)
        cls.get_telegram_block(cls.root)
        cls.get_testmem5_block(cls.root)
        cls.get_start_block(cls.root)
        cls.get_stop_block(cls.root)
        cls.get_buttons_block(cls.root)
        cls.get_logs_block(cls.root)
        return cls.root

    @staticmethod
    def get_main_window():
        from main import VERSION

        root = Tk()
        root.iconphoto(True, Icon.get_as_file())
        root.title(f'MOCT {VERSION}')
        w = 380
        h = 400
        x = int(root.winfo_screenwidth() / 2 - w / 2)
        y = int(root.winfo_screenheight() / 2 - h / 2)
        root.geometry(f'{w}x{h}+{x}+{y}')
        root.resizable(False, False)
        return root

    @classmethod
    def get_menu_bar(cls, root):
        menubar = Menu(root)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=cls.root.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="Help",
                               command=lambda: webbrowser.open_new('https://github.com/memoryoctool/MOCT/wiki'))
        about_menu.add_command(label="GutHub",
                               command=lambda: webbrowser.open_new('https://github.com/memoryoctool/MOCT'))
        about_menu.add_command(label="About", command=AboutGui.window)
        menubar.add_cascade(label="Help", menu=about_menu)

        root.config(menu=menubar)

    @classmethod
    def get_telegram_block(cls, root):
        Label(root, text="Telegram integration:").place(x=10, y=10)
        cls.telegram_status_entry = Entry(root)
        cls.telegram_status_entry.place(width=180, height=20, x=150, y=12)
        cls.update_telegram_status_entry()
        Button(root, text="...", command=cls.open_telegram_settings).place(width=20, height=20, x=340, y=12)

    @classmethod
    def update_telegram_status_entry(cls):
        cls.telegram_status_entry.config(state='normal')
        cls.telegram_status_entry.delete(0, END)
        cls.telegram_status_entry.insert(0, Notifier.get_telegram_status())
        cls.telegram_status_entry.config(state='disabled')

    @classmethod
    def open_telegram_settings(cls):
        TelegramSettingsGui.window()

    @classmethod
    def get_testmem5_block(cls, root):
        Label(root, text="TestMem5 location:").place(x=10, y=50)
        cls.testmem5_path_entry = Entry(root)
        cls.testmem5_path_entry.insert(0, Config.get_testmem5_path())
        cls.testmem5_path_entry.config(state='readonly')
        cls.testmem5_path_entry.place(width=180, height=20, x=150, y=52)
        Button(root, text="...", command=cls.select_testmem5_path).place(width=20, height=20, x=340, y=52)

    @classmethod
    def select_testmem5_path(cls):
        path = filedialog.askopenfilename(filetypes=(("Exe files", "*.exe"), ("all files", "*.*")))
        if not path:
            return
        Config.set_testmem5_path(path)
        cls.testmem5_path_entry.config(state='normal')
        cls.testmem5_path_entry.delete(0, END)
        cls.testmem5_path_entry.insert(0, Config.get_testmem5_path())
        cls.testmem5_path_entry.config(state='readonly')

    @classmethod
    def get_start_block(cls, root):
        cls.startup_checkbox_value = IntVar(root, Windows.is_startup_enabled())
        Checkbutton(root, variable=cls.startup_checkbox_value, command=cls.startup_change,
                    text="Start with windows").place(x=10, y=90)

        cls.test_on_startup_checkbox_value = IntVar(root, Config.get_run_tests_on_startup())
        Checkbutton(root, variable=cls.test_on_startup_checkbox_value, command=cls.test_on_startup_change,
                    text="Run tests when started").place(x=145, y=90)

    @classmethod
    def startup_change(cls):
        if cls.startup_checkbox_value.get():
            Windows.add_to_startup()
        else:
            Windows.remove_from_startup()

    @classmethod
    def test_on_startup_change(cls):
        Config.set_run_tests_on_startup(cls.test_on_startup_checkbox_value.get())

    @classmethod
    def get_stop_block(cls, root):
        cls.stop_on_errors_checkbox_value = IntVar(root, Config.get_stop_on_errors())
        Checkbutton(root, variable=cls.stop_on_errors_checkbox_value, command=cls.stop_on_errors_change,
                    text="Stop tests on errors").place(x=10, y=130)

    @classmethod
    def stop_on_errors_change(cls):
        Config.set_stop_on_errors(cls.stop_on_errors_checkbox_value.get())

    @classmethod
    def get_buttons_block(cls, root):
        cls.testmem5_run_tests_button_text = StringVar(root)
        Button(root, text="Start tests", command=cls.run_tests_clicked,
               textvariable=cls.testmem5_run_tests_button_text).place(width=80, height=24, x=10, y=170)
        cls.update_run_tests_text()
        Button(root, text="Reboot into BIOS", command=cls.reboot_clicked).place(width=120, height=24, x=110, y=170)

    @classmethod
    def run_tests_clicked(cls):
        MemTest.toggle_do_test()
        cls.update_run_tests_text()

    @classmethod
    def update_run_tests_text(cls):
        text = "Stop tests" if MemTest.do_test else "Start tests"
        cls.testmem5_run_tests_button_text.set(text)

    @classmethod
    def reboot_clicked(cls):
        if messagebox.askokcancel("MOCT", "Are you sure you want to reboot?"):
            Windows.reboot_into_bios()

    @classmethod
    def get_logs_block(cls, root):
        cls.logs_text = ScrolledText(root, wrap="word", font="Arial 9")
        cls.logs_text.place(width=360, height=180, x=10, y=210)
        cls.logs_text.insert("0.0", cls.logs)
        cls.logs_text.config(state='disabled')

    @classmethod
    def append_logs(cls, log):
        window_log_entry = datetime.now().strftime("%H:%M:%S ") + log + "\n"
        cls.logs += window_log_entry
        cls.logs_text.config(state='normal')
        cls.logs_text.insert(END, window_log_entry)
        cls.logs_text.config(state='disabled')
        cls.logs_text.yview_scroll(number=1, what="units")

        with open(cls.log_file, "a", encoding="utf-8") as f:
            f.write(datetime.now().strftime("%d.%m.%y %H:%M:%S ") + log + "\n")
