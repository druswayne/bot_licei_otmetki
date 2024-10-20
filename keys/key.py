from aiogram import types
from aiogram.types import WebAppInfo

kb_date = [
    types.InlineKeyboardButton(text="Сегодняшняя дата", callback_data="now"),
    types.InlineKeyboardButton(text="Другая дата", callback_data="other")]


kb_klass = [
    types.InlineKeyboardButton(text="10М1", callback_data="class-M1_10"),
    types.InlineKeyboardButton(text="10М2", callback_data="class-M2_10"),
    types.InlineKeyboardButton(text="10Г", callback_data="class-G_10"),
    types.InlineKeyboardButton(text="11М2", callback_data="class-M2_11"),
    types.InlineKeyboardButton(text="11Л", callback_data="class-L_11"),
    types.InlineKeyboardButton(text="11Ю", callback_data="class-UR_11")]
