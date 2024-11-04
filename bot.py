import json
import logging
import asyncio
from loader import *
import handler.admin
import handler.user
import datetime
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class SaveMessageMiddleware(BaseMiddleware):
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__()

    async def __call__(self, handler, event, data):
        message = event
        try:
            text = json.loads(message.json())['message']['text']
            id_user = json.loads(message.json())['message']['from_user']['id']
            date = datetime.datetime.now()
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(f"{date}      {id_user}     {text}\n")
        except Exception as e:
            logging.error(f"Failed to write message to file: {e}")

        return await handler(event, data)

file_path = 'messages.txt'
save_message_middleware = SaveMessageMiddleware(file_path)

dp.update.middleware.register(save_message_middleware)

async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(filename='errors.log',level=logging.ERROR)

    asyncio.run(main())