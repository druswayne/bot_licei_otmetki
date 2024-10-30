import logging
import asyncio
from loader import *
import handler.admin
import handler.user
async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(filename='errors.log',level=logging.ERROR)

    asyncio.run(main())