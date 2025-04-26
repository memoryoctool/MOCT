import webbrowser
from tkinter import *

from moct.config import Config
from moct.gui.icon import Icon


class AboutGui:
    root = None

    @classmethod
    def window(cls):
        cls.root = cls.get_main_window()
        cls.get_labels_block(cls.root)
        return cls.root

    @classmethod
    def get_main_window(cls):
        pos = ''
        last_window_x = Config.get_param('gui', 'about', 'x', throw=False)
        last_window_y = Config.get_param('gui', 'about', 'y', throw=False)
        if last_window_x and last_window_y:
            pos = f'+{last_window_x}+{last_window_y}'

        root = Toplevel()
        root.iconphoto(True, Icon.get_as_file())
        root.title('About')
        root.geometry(f'390x240{pos}')
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

            Config.set_param(x, 'gui', 'about', 'x')
            Config.set_param(y, 'gui', 'about', 'y')

        cls.root.grab_release()
        cls.root.destroy()

    @classmethod
    def get_labels_block(cls, root):
        from main import VERSION

        Label(root, text='MOCT (Memory OverClocking Tool)').place(x=10, y=10)
        Label(root, text=f'Version {VERSION}').place(x=10, y=30)

        Label(root, text='MOCT is an open-source project built for PC enthusiasts who want').place(x=10, y=70)
        Label(root, text='to unlock higher performance from their memory modules.').place(x=10, y=90)

        Label(root, text='GitHub:').place(x=10, y=130)
        gh = Label(root, text='https://github.com/memoryoctool/MOCT', fg="blue", cursor="hand2")
        gh.bind("<Button-1>", lambda e: webbrowser.open_new('https://github.com/memoryoctool/MOCT'))
        gh.place(x=55, y=130)
        Label(root, text='Documentation & Settings: Find detailed guides and tips in our ').place(x=10, y=150)
        wiki = Label(root, text='Wiki', fg="blue", cursor="hand2")
        wiki.bind("<Button-1>", lambda e: webbrowser.open_new('https://github.com/memoryoctool/MOCT/wiki'))
        wiki.place(x=345, y=150)
        Label(root, text='Community & Support: Have feedback or feature requests? Join our').place(x=10, y=170)
        Label(root, text='Discord community — look for the link in the GitHub repository.').place(x=10, y=190)
