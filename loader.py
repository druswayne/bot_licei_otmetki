from aiogram import Bot, Dispatcher, Router, F
import sqlite3

from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = '7897854042:AAFY-hKwxyuDu8iMGRvdWN5Ry7xsl6G-T-k'
con = sqlite3.connect("data.db")
cursor = con.cursor()
router = Router()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)
state_data = {}