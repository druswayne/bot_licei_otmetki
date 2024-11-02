import json

import requests
from aiogram import Bot, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from keys.key import kb_soglas, kb_choice
from loader import router, cursor, con


class Form_name(StatesGroup):
    choice = State()
    token = State()


def req(zapros, data):
    zapros = json.dumps(zapros)
    data = json.dumps(data)
    url = f'https://druswayne.pythonanywhere.com/get_data_db/?request={zapros}&data={data}'
    data = requests.get(url)
    data_decode = json.loads(data.content)

    return data_decode


@router.message(Command('start'))
async def reg(message: Message, bot: Bot, state: FSMContext) -> None:
    # уникальный токен
    # https://t.me/collab_bot?start=кеекекеек
    token = message.text.split()[-1].split('_')[-1]
    user_id = message.chat.id

    try:
        token_db = req("SELECT token FROM users WHERE id=(?)", [user_id])
        if token != '/start' and token != token_db[0][0]:
            await message.answer(text='Аккаунт уже привязан к журналу.\nЧтобы отвязать аккаунт используйте команду /delete')
            return

    except:
        pass
    try:
        id_token = req("SELECT id FROM users WHERE token=(?)", [token])[0][0]
        if str(id_token).isdigit():
            await message.answer(
                text='Упс\nТакой пользователь уже зарегистрировался')
            return
    except:
        pass
    data = req("SELECT * FROM users WHERE id=(?)", [user_id])
    if len(data) != 0:
        builder = ReplyKeyboardBuilder()
        for button in kb_choice:
            builder.add(button)
        builder.adjust(1)
        await message.answer(text='🤓', reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        if token == '/start':
            await message.answer(text='Отсканируй QR-код для регистрации.')
            return

        name = req("SELECT name FROM users WHERE token=(?)", [token])[0][0]
        builder = ReplyKeyboardBuilder()
        for button in kb_soglas:
            builder.add(button)
        builder.adjust(1)
        await state.set_state(Form_name.token)
        await state.update_data(token=token)
        await state.set_state(Form_name.choice)
        await message.answer(text=f'Привет!\n{name} – это ты?',
                             reply_markup=builder.as_markup(resize_keyboard=True))




@router.message(Form_name.choice)
async def choice(message: Message, bot, state: FSMContext):
    await state.update_data(choice=message.text)
    data_date = await state.get_data()
    choice = data_date['choice']
    token = data_date['token']
    await state.clear()
    if choice == "Да, это я":
        req('UPDATE users SET id=(?) WHERE token=(?)', [message.chat.id, token])

        builder = ReplyKeyboardBuilder()
        for button in kb_choice:
            builder.add(button)
        builder.adjust(1)
        await message.answer(text='Поздравляю, ты зарегистрирован!',
                             reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await message.answer('Отсканируй QR-код заново', reply_markup=types.ReplyKeyboardRemove())

@router.message(Command('stats'))
@router.message(F.text == 'Посмотреть свои отметки')
async def get_stats(message: Message):
    user_id = message.chat.id
    data = req("SELECT * FROM users WHERE id=(?)", [user_id])
    if len(data) == 0:
        await message.answer('Отсканируй QR-код для регистрации')
        return
    id_user = message.chat.id

    data = req('SELECT klass from users WHERE id=(?)', [id_user])
    if not len(data):
        await message.answer(text='Отсканируй QR-код для регистрации!')
        return
    klass = data[0][0]

    name = req('SELECT name from users WHERE id=(?)', [id_user])[0][0]
    url = f'https://druswayne.pythonanywhere.com/get_stats/?klass={klass}&name={name}'
    data = json.loads(requests.get(url).content)
    try:
        average = round(sum(data) / len(data), 2)
    except:
        average = 0
    text = ''
    for i in data:
        text += f'{i}, '
    text = text[:-2]
    await message.answer(f'{name}, твои отметки по математике: {text}\nСредний балл: {average}')

@router.message(Command('delete'))
async def del_user(message: Message):
    id_user = message.chat.id
    data = req('SELECT klass from users WHERE id=(?)', [id_user])
    if not len(data):
        await message.answer(text='Ваш аккаунт не привязан к журналу!')
        return
    req("UPDATE users SET id=NULL WHERE id=(?)", [id_user])
    await message.answer(text='Ваш аккаунт отвязан от журнала!')