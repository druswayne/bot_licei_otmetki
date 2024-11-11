import json

from aiogram import F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, WebAppInfo, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import requests
from json import loads



from keys.key import kb_date, kb_klass, kb_klass_mess, kb_send_photo, kb_choice_mess
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
    qwest = State()
    photo_flag = State()
    photo = State()


@router.message(Command('cancel'))
async def cancel(message: Message, bot: Bot, state: FSMContext):
    await state.clear()

    await bot.send_message(chat_id=731866035, text='Действие отменено', reply_markup=types.ReplyKeyboardRemove())


@router.message(Command('qwest'))
async def set_qwest(message: Message, bot: Bot) -> None:
    user_id = message.chat.id
    if user_id == 731866035:
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text='открыть', web_app=WebAppInfo(
            url=f"https://druswayne.pythonanywhere.com/qwest/")))
        await bot.send_message(chat_id=731866035,
                               text='Редактор квеста',
                               reply_markup=builder.as_markup(resize_keyboard=True),
                               )


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
    await state.set_state(Form_mess.qwest)
    builder = ReplyKeyboardBuilder()
    for button in kb_choice_mess:
        builder.add(button)
    builder.adjust(1)
    await bot.send_message(chat_id=731866035, text='что отправляем?',
                           reply_markup=builder.as_markup(resize_keyboard=True)
                           )


@router.message(Form_mess.qwest)
async def choice_mess_type(message: Message, bot: Bot, state: FSMContext):
    if message.text == 'Текст':
        await state.set_state(Form_mess.text)
        await bot.send_message(chat_id=731866035, text='что отправляем?', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Квест':
        url = f'https://druswayne.pythonanywhere.com/static/qwest.json'
        data = json.loads(requests.get(url).text)
        text = data['text']
        file = data['file_image']
        await state.clear()
        if state_data['class'] == '666':
            data_users = req("SELECT id FROM users", [])
        else:
            data_users = req("SELECT id FROM users WHERE klass=(?)", [state_data['class']])
        if file != None:
            data_image = requests.get(f'https://druswayne.pythonanywhere.com{file}')
            if data_image.status_code == 200:
                with open("image/downloaded_image.jpg", "wb") as file:
                    file.write(data_image.content)
                image = FSInputFile("image/downloaded_image.jpg")


                for user in data_users:
                    try:

                        await bot.send_photo(chat_id=user[0], photo=image)
                    except:
                        pass

        correct_answer = data['correct_answer']
        list_option = data['list_option']
        question_hint = data['question_hint']
        count_mess = 0
        for user in data_users:
            try:

                await bot.send_poll(type='quiz', question=text,
                                    options=list_option,
                                    correct_option_id=correct_answer,
                                    chat_id=user[0],
                                    explanation=question_hint)
                count_mess += 1
            except:
                pass

        await bot.send_message(chat_id=731866035, text=f'Квесты отправлены!\n{count_mess}',
                               reply_markup=types.ReplyKeyboardRemove())


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
        if state_data['class'] == '666':
            data_users = req("SELECT id FROM users", [])
        else:
            data_users = req("SELECT id FROM users WHERE klass=(?)", [state_data['class']])
        count_mess = 0
        for user in data_users:
            try:

                await bot.send_message(chat_id=user[0], text=f'Письмо от наставника:\n{text_mess}')
                count_mess += 1
            except:
                pass
        await bot.send_message(chat_id=731866035, text=f'Письма отправлены!\n{count_mess}',
                               reply_markup=types.ReplyKeyboardRemove())
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

    if state_data['class'] == '666':
        data_users = req("SELECT id FROM users", [])

    else:
        data_users = req("SELECT id FROM users WHERE klass=(?)", [state_data['class']])
    count_mess = 0
    for user in data_users:
        try:

            await bot.send_photo(chat_id=user[0], photo=photo, caption=f'Письмо от наставника:\n{text_mess}')
            count_mess += 1
        except:
            pass
    await bot.send_message(chat_id=731866035, text=f'Письма отправлены!\n{count_mess}',
                           reply_markup=types.ReplyKeyboardRemove())


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
    date = f"date_{datetime.datetime.now().day:02}_{month[datetime.datetime.now().month]:02}"
    print(date)
    # date = 'date_04_ноя'
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
    date = f'date_{data_date["date"]}'
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
