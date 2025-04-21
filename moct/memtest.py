import os
import subprocess
import subprocess as sp
from time import sleep

from pywinauto import Application

from moct.config import Config
from moct.notifyer import Notifier
from moct.windows import Windows


class MemTest:
    do_test = None
    testmem5 = None
    testmem5_window = None

    @classmethod
    def worker(cls):
        from moct.gui.main import MainGui

        if cls.do_test:
            MainGui.append_logs('Running memory tests in 5 sec.')
            sleep(5)
        else:
            frequency = cls.get_current_memory_frequency()
            MainGui.append_logs(f'Memory frequency is {frequency} MHz')

        while True:
            if not cls.do_test:
                sleep(0.1)
                continue

            MainGui.append_logs('Running memory tests...')

            frequency = cls.get_current_memory_frequency()
            if cls.is_current_frequency_was_reset_to_default():
                MainGui.append_logs(f'Memory frequency is {frequency} MHz, seems bad')
                Notifier.notify(f'Memory was reset to default frequency {frequency} MHz')
            else:
                MainGui.append_logs(f'Memory frequency is {frequency} MHz')

            can_reboot = True
            result = cls.run_testmem5()
            if result == 1:
                Notifier.notify("Tests failed")
            elif result == 2:
                can_reboot = False
            elif result == 3:
                MainGui.append_logs("TM5 window was closed")
                can_reboot = False

            cls.do_test = False
            MainGui.update_run_tests_text()

            if can_reboot:
                MainGui.append_logs("Rebooting into BIOS in 5 sec.")
                sleep(5)
                Windows.reboot_into_bios()

    @classmethod
    def run_testmem5(cls):
        from moct.gui.main import MainGui

        MainGui.append_logs("Running memory tests with TM5")

        testmem5_path = Config.get_testmem5_path()
        if not testmem5_path or not os.path.exists(testmem5_path):
            Notifier.notify("Can not run TM5: bad path")
            return 1

        # Trying to connect to existing TM5 process
        try:
            cls.testmem5 = Application(backend="uia").connect(path=Config.get_testmem5_path(), timeout=0)
            cls.testmem5_window = cls.testmem5.window()
        except:
            pass

        # Starting new TM5 process
        if cls.testmem5_window is None:
            sp.Popen([testmem5_path], stdin=sp.PIPE)
            try:
                cls.testmem5 = Application(backend="uia").connect(path=Config.get_testmem5_path(), timeout=5)
                cls.testmem5_window = cls.testmem5.window()
            except:
                Notifier.notify("Could not find TM5 window")
                cls.kill_tm5()
                return 3

        window_title = cls.testmem5_window.window_text()
        if not window_title.startswith('TestMem5'):
            MainGui.append_logs("Could not find TM5 window")
            cls.kill_tm5()
            return 2

        if '0.13.' not in window_title:
            MainGui.append_logs("Please use version 0.13.x of TestMem5")
            cls.kill_tm5()
            return 2

        last_whea_error_timestamp = Windows.get_last_whea_error_timestamp()
        time_from_last_check = 0
        check_interval = 10
        frequency = cls.get_current_memory_frequency()
        while True:
            sleep(0.1)
            if not cls.do_test:
                MainGui.append_logs('TM5 was stopped')
                cls.kill_tm5()
                return 2
            time_from_last_check += 0.1
            if time_from_last_check < check_interval:
                continue
            time_from_last_check = 0

            if not cls.testmem5_window.exists():
                try:
                    cls.testmem5_window = (Application(backend="uia").connect(path=Config.get_testmem5_path(), timeout=5)
                                       .window())
                except:
                    cls.kill_tm5()
                    return 3

            new_whea_errors = Windows.get_whea_errors_count_since(last_whea_error_timestamp)
            if new_whea_errors > 0:
                Notifier.notify(f"Found new WHEA errors ({frequency} MHz)")
                cls.kill_tm5()
                return 1

            stats = cls.get_testmem5_stats_from_window()

            if int(stats['errors']) > 0:
                Notifier.notify(
                    f"Memory test failed with {stats['errors']} errors on {stats['elapsed']}, config: {stats['config']}")
                cls.kill_tm5()
                return 1
            elif stats['status'] == 'completed':
                Notifier.notify(f"Testing completed with no errors. Tests: {stats['test']}, cycle: {stats['cycle']}, elapsed: {stats['elapsed']}, config: {stats['config']}.")
                break

        cls.kill_tm5()
        return 0

    @classmethod
    def toggle_do_test(cls):
        cls.do_test = not cls.do_test

    @classmethod
    def kill_tm5(cls):
        if cls.testmem5:
            cls.testmem5.kill()
            cls.testmem5 = None
            cls.testmem5_window = None

    @classmethod
    def get_testmem5_stats_from_window(cls):
        stats = {'config': '', 'elapsed': '0:00:00', 'cycle': '0', 'test': '0 / 0', 'errors': '0', 'status': ''}
        next_is = None

        try:
            children = cls.testmem5_window.children()
        except:
            return stats

        for child in children:
            windows_text = child.window_text()
            if next_is is not None:
                stats[next_is] = windows_text
                next_is = None
            elif windows_text == 'Configuration' or windows_text == 'Конфигурация':
                next_is = 'config'
            elif windows_text == 'Elapsed' or windows_text == 'Прошло':
                next_is = 'elapsed'
            elif windows_text == 'Cycle' or windows_text == 'Цикл':
                next_is = 'cycle'
            elif windows_text == 'Test' or windows_text == 'Тест':
                next_is = 'test'
            elif windows_text == 'Errors' or windows_text == 'Ошибок':
                next_is = 'errors'
            elif windows_text == 'Testing completed' or windows_text == 'Тестирование закончено':
                stats['status'] = 'completed'

        return stats

    @classmethod
    def is_current_frequency_was_reset_to_default(cls):
        return cls.get_current_memory_frequency() in Config.get_default_memory_frequencies()

    @staticmethod
    def get_current_memory_frequency():
        cmd = ["wmic", "memorychip", "get", "speed"]
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode("utf-8", errors="ignore").strip().split("\n")

        return int(lines[-1])
