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


kb_klass_mess = [
    types.InlineKeyboardButton(text="10М1", callback_data="mess-M1_10"),
    types.InlineKeyboardButton(text="10М2", callback_data="mess-M2_10"),
    types.InlineKeyboardButton(text="10Г", callback_data="mess-G_10"),
    types.InlineKeyboardButton(text="11М2", callback_data="mess-M2_11"),
    types.InlineKeyboardButton(text="11Л", callback_data="mess-L_11"),
    types.InlineKeyboardButton(text="11Ю", callback_data="mess-UR_11"),
    types.InlineKeyboardButton(text="всем", callback_data="mess-666")]

kb_choice_mess = [
    types.KeyboardButton(text='Текст'),
    types.KeyboardButton(text='Квест')
]

kb_send_photo = [
    types.KeyboardButton(text='Да'),
    types.KeyboardButton(text='Нет')]

kb_soglas = [
    types.KeyboardButton(text='Да, это я'),
    types.KeyboardButton(text='Нет, это не я')]

kb_choice = [
    types.KeyboardButton(text='Посмотреть свои отметки')]