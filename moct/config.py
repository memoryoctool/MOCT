import os

import yaml


class Config:
    file = 'moct.conf.yaml'
    params = None
    default_params = {
        'telegram': {
            'bot_token': '',
            'chat_id': '',
        },
        'testmem5': {
            'path': '',
            'stop_on_errors': True,
        },
        'run_tests_on_startup': False,
        'default_memory_frequencies': [2133, 2666],
    }

    @classmethod
    def get(cls):
        if cls.params is None:
            cls.params = cls.default_params

            if os.path.exists(cls.file):
                with open(cls.file) as stream:
                    try:
                        cls.params = yaml.safe_load(stream)
                    except yaml.YAMLError:
                        pass

        return cls.params

    @classmethod
    def save(cls, params):
        cls.params = params
        with open(cls.file, 'w') as stream:
            stream.write(yaml.dump(params))

    @classmethod
    def get_param(cls, *path, throw=True):
        def find_in_config(config_dict):
            current = config_dict
            for i, key in enumerate(path):
                if key not in current:
                    return None
                if i == len(path) - 1:
                    return current[key]
                current = current[key]
            return None

        result = find_in_config(cls.get())
        if result is not None:
            return result

        result = find_in_config(cls.default_params)
        if result is not None:
            return result

        if throw:
            raise ValueError(f'Path {path} is not found in config')

        return None

    @classmethod
    def set_param(cls, value, *path):
        if not path:
            raise ValueError("Path cannot be empty")

        params = cls.get()
        current = params

        for i, key in enumerate(path):
            if i == len(path) - 1:
                current[key] = value
            else:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]

        cls.save(params)

        return value

    @classmethod
    def get_run_tests_on_startup(cls):
        return bool(cls.get_param('run_tests_on_startup'))

    @classmethod
    def set_run_tests_on_startup(cls, value):
        cls.set_param(bool(value), 'run_tests_on_startup')

    @classmethod
    def get_telegram_bot_token(cls):
        return cls.get_param('telegram', 'bot_token')

    @classmethod
    def set_telegram_bot_token(cls, token):
        cls.set_param(str(token), 'telegram', 'bot_token')

    @classmethod
    def get_telegram_chat_id(cls):
        return cls.get_param('telegram', 'chat_id')

    @classmethod
    def set_telegram_chat_id(cls, chat_id):
        cls.set_param(str(chat_id), 'telegram', 'chat_id')

    @classmethod
    def get_testmem5_path(cls):
        return cls.get_param('testmem5', 'path')

    @classmethod
    def set_testmem5_path(cls, path):
        cls.set_param(str(path), 'testmem5', 'path')

    @classmethod
    def get_stop_on_errors(cls):
        return cls.get_param('testmem5', 'stop_on_errors')

    @classmethod
    def set_stop_on_errors(cls, stop_on_errors):
        cls.set_param(bool(stop_on_errors), 'testmem5', 'stop_on_errors')

    @classmethod
    def get_default_memory_frequencies(cls):
        return cls.get_param('default_memory_frequencies')
