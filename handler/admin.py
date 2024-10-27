from aiogram import F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import requests
from json import loads
from keys.key import kb_date, kb_klass, kb_klass_mess, kb_send_photo
from loader import router, state_data
import datetime
from handler.user import req

month = {1: "янв",
         2: "фев",
         3: "мар",
         4: "апр",
         5: "май",
         6: "июн",
         7: "июл",
         8: "авг",
         9: "сен",
         10: "окт",
         11: "ноя",
         12: "дек",
         }


class Form_date(StatesGroup):
    date = State()


class Form_mess(StatesGroup):
    text = State()
    photo_flag = State()
    photo = State()


@router.message(Command('cancel'))
async def cancel(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.send_message(chat_id=731866035, text='Действие отменено')


@router.message(Command('mess'))
async def send_mess(message: Message, bot: Bot) -> None:
    user_id = message.chat.id
    if user_id == 731866035:
        # for i in range(message.message_id, 0, -1):
        #    try:
        #        await bot.delete_message(message.from_user.id, i)
        #    except:
        #        continue
        message_1 = await message.answer('Чего изволишь, хозяин?', reply_markup=types.ReplyKeyboardRemove())
        builder = InlineKeyboardBuilder()
        for button in kb_klass_mess:
            builder.add(button)
        builder.adjust(3)

        message = await message.answer('Какой класс?',
                                       reply_markup=builder.as_markup(resize_keyboard=True))
        state_data['mess'] = message.message_id
        state_data['mess1'] = message_1.message_id
    else:
        await message.answer('Нет доступа.')


@router.callback_query(F.data.startswith("mess"))
async def get_text(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    # await bot.delete_message(chat_id=731866035, message_id=state_data['mess'])
    # await bot.delete_message(chat_id=731866035, message_id=state_data['mess1'])
    del state_data['mess']
    del state_data['mess1']
    klass = callback.data.split('-')[1]
    state_data['class'] = klass
    await state.set_state(Form_mess.text)
    await bot.send_message(chat_id=731866035, text='Что отправляем?')


@router.message(Form_mess.text)
async def page_other_date(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Form_mess.photo_flag)
    builder = ReplyKeyboardBuilder()
    for button in kb_send_photo:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='Отправляем фото?',
                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(Form_mess.photo_flag)
async def flag_photo(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(photo_flag=message.text)
    if message.text == "Нет":
        data = await state.get_data()
        text_mess = data['text']
        data_users = req("SELECT id FROM users WHERE klass=(?)", [state_data['class']])
        for user in data_users:
            try:
                await bot.send_message(chat_id=user[0], text=f'Письмо от наставника:\n{text_mess}')
            except:
                pass
        await bot.send_message(chat_id=731866035, text='Письма отправлены!', reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    await state.set_state(Form_mess.photo)
    await message.answer(text='Отправляй фотку', reply_markup=types.ReplyKeyboardRemove())


@router.message(Form_mess.photo)
async def send_mess_photo(message: Message, bot: Bot, state: FSMContext):
    photo = message.photo[0].file_id
    data = await state.get_data()
    text_mess = data['text']
    await state.clear()
    data_users = req("SELECT id FROM users WHERE klass=(?)", [state_data['class']])
    for user in data_users:
        try:
            await bot.send_photo(chat_id=user[0], photo=photo, caption=f'Письмо от наставника:\n{text_mess}')
        except:
            pass
    await bot.send_message(chat_id=731866035, text='Письма отправлены!', reply_markup=types.ReplyKeyboardRemove())


@router.message(Command('grade'))
async def get_class(message: Message, bot: Bot) -> None:
    user_id = message.chat.id
    if user_id == 731866035:
        # for i in range(message.message_id, 0, -1):
        #    try:
        #        await bot.delete_message(message.from_user.id, i)
        #    except:
        #        continue
        message_1 = await message.answer('Чего изволишь, хозяин?', reply_markup=types.ReplyKeyboardRemove())
        builder = InlineKeyboardBuilder()
        for button in kb_klass:
            builder.add(button)
        builder.adjust(3)

        message = await message.answer('Какой класс?',
                                       reply_markup=builder.as_markup(resize_keyboard=True))
        state_data['mess'] = message.message_id
        state_data['mess1'] = message_1.message_id
    else:
        await message.answer('Нет доступа.')


@router.callback_query(F.data.startswith("class"))
async def choice_date(callback: types.CallbackQuery, bot: Bot):
    # await bot.delete_message(chat_id=731866035, message_id=state_data['mess'])
    # await bot.delete_message(chat_id=731866035, message_id=state_data['mess1'])
    del state_data['mess']
    del state_data['mess1']
    klass = callback.data.split('-')[1]
    state_data['class'] = klass
    # date = f"date_{datetime.datetime.now().day}_{month[datetime.datetime.now().month]}"
    date = 'date_04_ноя'
    url = f'https://druswayne.pythonanywhere.com/getdate/?date={date}&klass={klass}'
    data = requests.get(url)

    builder = InlineKeyboardBuilder()
    for date in loads(data.content):
        button = types.InlineKeyboardButton(text=f"{date[5:]}", callback_data=date)
        builder.add(button)
    button = types.InlineKeyboardButton(text=f"другая", callback_data='other')
    builder.add(button)
    builder.adjust(1)
    message = await bot.send_message(chat_id=731866035,
                                     text='Выбери дату',
                                     reply_markup=builder.as_markup(resize_keyboard=True))
    state_data['mess'] = message.message_id


@router.callback_query(F.data.startswith("date"))
async def get_page(callback: types.CallbackQuery, bot: Bot):
    # await bot.delete_message(chat_id=731866035, message_id=state_data['mess'])
    del state_data['mess']
    date = callback.data
    klass = state_data['class']
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='открыть', web_app=WebAppInfo(
        url=f"https://druswayne.pythonanywhere.com/date/?date={date}&klass={klass}")))
    builder.adjust(4)
    del state_data['class']

    await bot.send_message(chat_id=731866035,
                           text='Можно открывать таблицу',
                           reply_markup=builder.as_markup(resize_keyboard=True),
                           )


@router.callback_query(F.data == "other")
async def get_other_data(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Form_date.date)
    await bot.send_message(chat_id=731866035, text='отправь дату в формате дд_ммм (11_ноя)')


@router.message(Form_date.date)
async def page_other_date(message: Message, bot, state: FSMContext):
    await state.update_data(date=message.text)
    data_date = await state.get_data()
    date = f'date_{data_date['date']}'
    await state.clear()
    klass = state_data['class']
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='открыть', web_app=WebAppInfo(
        url=f"https://druswayne.pythonanywhere.com/date/?date={date}&klass={klass}")))
    builder.adjust(4)
    del state_data['class']

    await bot.send_message(chat_id=731866035,
                           text='Можно открывать таблицу',
                           reply_markup=builder.as_markup(resize_keyboard=True),
                           )
