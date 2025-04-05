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
    def get_run_tests_on_startup(cls):
        params = cls.get()
        if 'run_tests_on_startup' in params:
            return bool(params['run_tests_on_startup'])
        return bool(cls.default_params['run_tests_on_startup'])

    @classmethod
    def set_run_tests_on_startup(cls, value):
        params = cls.get()
        params['run_tests_on_startup'] = bool(value)
        cls.save(params)

    @classmethod
    def get_telegram_bot_token(cls):
        params = cls.get()
        if 'telegram' in params:
            if 'bot_token' in params['telegram']:
                return params['telegram']['bot_token']
        return cls.default_params['telegram']['bot_token']

    @classmethod
    def set_telegram_bot_token(cls, token):
        params = cls.get()
        if 'telegram' not in params:
            params['telegram'] = cls.default_params['telegram']
        params['telegram']['bot_token'] = str(token)
        cls.save(params)

    @classmethod
    def get_telegram_chat_id(cls):
        params = cls.get()
        if 'telegram' in params:
            if 'chat_id' in params['telegram']:
                return params['telegram']['chat_id']
        return cls.default_params['telegram']['chat_id']

    @classmethod
    def set_telegram_chat_id(cls, chat_id):
        params = cls.get()
        if 'telegram' not in params:
            params['telegram'] = cls.default_params['telegram']
        params['telegram']['chat_id'] = str(chat_id)
        cls.save(params)

    @classmethod
    def get_testmem5_path(cls):
        params = cls.get()
        if 'testmem5' in params:
            if 'path' in params['testmem5']:
                return params['testmem5']['path']
        return cls.default_params['testmem5']['path']

    @classmethod
    def set_testmem5_path(cls, path):
        params = cls.get()
        if 'testmem5' not in params:
            params['testmem5'] = cls.default_params['testmem5']
        params['testmem5']['path'] = str(path)
        cls.save(params)

    @classmethod
    def get_stop_on_errors(cls):
        params = cls.get()
        if 'testmem5' in params:
            if 'stop_on_errors' in params['testmem5']:
                return params['testmem5']['stop_on_errors']
        return cls.default_params['testmem5']['stop_on_errors']

    @classmethod
    def set_stop_on_errors(cls, stop_on_errors):
        params = cls.get()
        if 'testmem5' not in params:
            params['testmem5'] = cls.default_params['testmem5']
        params['testmem5']['stop_on_errors'] = bool(stop_on_errors)
        cls.save(params)

    @classmethod
    def get_default_memory_frequencies(cls):
        params = cls.get()
        if 'default_memory_frequencies' in params:
            return params['default_memory_frequencies']
        return cls.default_params['default_memory_frequencies']
