import asyncio
from time import sleep
from tkinter import messagebox

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from moct.config import Config


class Notifier:
    bot_instance = None

    worker_queue = []

    @classmethod
    def worker(cls):
        from moct.gui.main import MainGui

        loop = asyncio.new_event_loop()

        while True:
            if len(cls.worker_queue):
                task = cls.worker_queue.pop(0)
                try:
                    loop.run_until_complete(task[0](*task[1]))
                except Exception as e:
                    MainGui.append_logs(f"[Error] {e}")

            sleep(0.01)

    @classmethod
    def bot(cls):
        if cls.bot_instance is None:
            cls.bot_instance = Bot(token=Config.get_telegram_bot_token(),
                                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        return cls.bot_instance

    @classmethod
    def update_bot_instance(cls):
        cls.worker_queue.append((cls._update_bot_instance_coroutine, []))

    @classmethod
    async def _update_bot_instance_coroutine(cls):
        if cls.bot_instance is not None:
            await cls.bot_instance.session.close()
            cls.bot_instance = None

    @classmethod
    def notify(cls, message):
        from moct.gui.main import MainGui

        MainGui.append_logs(f"[Message] {message}")
        cls.worker_queue.append([cls.bot().send_message, [Config.get_telegram_chat_id(), message]])

    @staticmethod
    def get_telegram_status():
        if Config.get_telegram_bot_token() and Config.get_telegram_chat_id():
            return 'enabled'
        return 'not configured'

    @staticmethod
    async def send_test_message(token, chat_id):
        bot = Bot(token=token)
        try:
            await bot.send_message(chat_id=chat_id, text='Test message from settings')
            messagebox.showinfo("MOCT", "Message sent successfully")
        except Exception as e:
            messagebox.showerror("MOCT", e)
        await bot.session.close()
