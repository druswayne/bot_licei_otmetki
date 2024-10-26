from aiogram import Bot, Dispatcher, Router, F
import sqlite3

from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = '7385714840:AAHlyQdM85RjBl7pklB0mAGlU7d6AYy1950'
con = sqlite3.connect("data.db")
cursor = con.cursor()
router = Router()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)
state_data = {}