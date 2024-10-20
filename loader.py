from aiogram import Bot, Dispatcher, Router, F
import sqlite3

from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = '7385714840:AAGboUJkVyGK-XD0hdzC54qYsi9OTi9Mygo'
con = sqlite3.connect("data.db")
cursor = con.cursor()
router = Router()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)
state_data = {}