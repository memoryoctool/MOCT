import getpass
import os
import sys

import win32com.client
import win32evtlog
import win32security


class Windows:
    @staticmethod
    def get_program_path():
        return sys.executable

    @classmethod
    def is_compiled(cls):
        return cls.get_program_path().split('\\')[-1] != 'python.exe'

    @classmethod
    def is_startup_enabled(cls):
        if not cls.is_compiled():
            return False

        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_folder = scheduler.GetFolder('\\')
        try:
            task = root_folder.GetTask('MOCT')
        except Exception:
            return False

        should_reinstall_task = True
        for action in task.Definition.Actions:
            if action.Type == win32com.client.constants.TASK_ACTION_EXEC:
                exec_action = win32com.client.CastTo(action, "IExecAction")
                if exec_action.Path == cls.get_program_path():
                    should_reinstall_task = False

        # If exe was moved we should change the path
        if should_reinstall_task:
            cls.remove_from_startup()
            cls.add_to_startup()

        return True

    @staticmethod
    def get_current_user_id():
        return f"{os.environ['USERDOMAIN']}\\{getpass.getuser()}"

    @staticmethod
    def get_current_user_sid():
        username = getpass.getuser()
        domain = os.environ['USERDOMAIN']
        user, domain, type = win32security.LookupAccountName(None, username)
        sid = win32security.ConvertSidToStringSid(user)
        return sid

    @classmethod
    def add_to_startup(cls):
        if not cls.is_compiled():
            return

        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_folder = scheduler.GetFolder('\\')
        task_def = scheduler.NewTask(0)
        task_def.RegistrationInfo.Description = 'MOCT - Memory OverClocking Tool https://github.com/memoryoctool/MOCT'
        task_def.RegistrationInfo.Author = cls.get_current_user_id()
        task_def.Settings.Compatibility = 6
        trigger_generic = task_def.Triggers.Create(9)
        trigger = win32com.client.CastTo(trigger_generic, "ILogonTrigger")
        trigger.Enabled = True
        trigger.UserId = cls.get_current_user_id()
        principal = task_def.Principal
        principal.UserId = cls.get_current_user_sid()
        principal.LogonType = 3
        principal.RunLevel = win32com.client.constants.TASK_RUNLEVEL_HIGHEST
        settings = task_def.Settings
        settings.Enabled = True
        settings.StartWhenAvailable = True
        settings.AllowHardTerminate = True
        settings.ExecutionTimeLimit = 'PT0S'
        settings.Priority = 7
        settings.MultipleInstances = 0
        settings.DisallowStartIfOnBatteries = False
        settings.StopIfGoingOnBatteries = False
        settings.RestartInterval = "PT1M"
        settings.RestartCount = 1
        settings.Hidden = False
        settings.RunOnlyIfIdle = False
        settings.WakeToRun = False
        idle_settings = settings.IdleSettings
        idle_settings.StopOnIdleEnd = True
        idle_settings.RestartOnIdle = False
        task_def.Actions.Context = 'Author'
        action = task_def.Actions.Create(win32com.client.constants.TASK_ACTION_EXEC)
        exec_action = win32com.client.CastTo(action, "IExecAction")
        exec_action.Path = cls.get_program_path()
        exec_action.WorkingDirectory = os.getcwd()
        try:
            root_folder.RegisterTaskDefinition('MOCT', task_def, 6, None, None, 3, None)
        except Exception as e:
            pass

    @classmethod
    def remove_from_startup(cls):
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_folder = scheduler.GetFolder('\\')
        try:
            root_folder.DeleteTask('MOCT', 0)
        except Exception:
            pass

    @staticmethod
    def reboot_into_bios():
        os.system('shutdown /r /fw /t 0 /f')

    @staticmethod
    def read_events_from_windows_log():
        handle = win32evtlog.OpenEventLog('localhost', 'System')
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_ERROR_TYPE
        return win32evtlog.ReadEventLog(handle, flags, 0)

    @classmethod
    def get_last_whea_error_timestamp(cls):
        events = cls.read_events_from_windows_log()
        for event in events:
            if event.SourceName.find("WHEA") != -1:
                return event.TimeGenerated.timestamp()
        return 0

    @classmethod
    def get_whea_errors_count_since(cls, timestamp):
        count = 0
        events = cls.read_events_from_windows_log()
        for event in events:
            if event.SourceName.find("WHEA") != -1 and event.TimeGenerated.timestamp() > timestamp:
                count += 1
        return count
