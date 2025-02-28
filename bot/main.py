from aiogram import Bot, types
from aiogram.types import InputMediaPhoto, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os, logging, sqlite3
import random, asyncio, schedule
import threading, datetime, math


#Модули проекта
from keyboards import kb  #Клавиатуры
from textbot import text_bot as tx  #Текст
from misc import misc as mc  #Доп функции

TOKEN = '6002429479:AAFCmsTfmLYkQ-gnt4MImb3Za6TRJd9tHzQ'
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

film_db = sqlite3.connect('./database/database.db')
film_cur = film_db.cursor()


last_send_message = None
viewed_message = []
history_id = []
no_update_urls = []
last_film = []
output = []
Genre = ""
Country = ""
Year = ""
Rating = ""
index = 1
Search = 'ID'



# запоминаем chat_id и message_id
# удаляем сообщение пользователя
# создаем новое сообщение
# делаем запрос к БД по chat_id, получаем message_id и удаляем это сообщение
# Меняем данные message_id в БД по chat_id
# Отправляем новое сообщение
#
#
#
#
#


#Обработка команд
@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    global last_send_message
    await mc.delete_message(bot, msg.from_user.id, msg.message_id)
    text_for_send = f"{tx.KB_MAIN_TEXT.hello}, {msg.from_user.full_name}!\nЯ - Cinema Everyday, телеграмм бот который," \
           f" поможет тебе с подбором фильма на вечер, чтобы начать пользоваться моим функционалом - отправь " \
           f"мне сообщение /menu"
    last_send_message = await msg.answer(text=text_for_send)
    user_id = msg.from_user.id
    if os.path.exists(f'./users/{user_id}.db') == False:
        mc.create_database(user_id)
    db = sqlite3.connect(f"./users/{msg.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text_for_send
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.message_handler(commands=['menu'])
async def start_menu(msg: types.Message):
    global last_send_message
    if msg.photo:
        await last_send_message.delete()
        last_send_message = await msg.answer(tx.KB_MAIN_TEXT.header.format(name=msg.from_user.full_name), reply_markup=kb.menu_kb1)
    else:
        await mc.delete_message(bot, msg.from_user.id, msg.message_id)
        last_send_message = await last_send_message.edit_text(text=tx.KB_MAIN_TEXT.header.format(name=msg.from_user.full_name),
                                             reply_markup=kb.menu_kb1)
    db = sqlite3.connect(f"./users/{msg.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()





















# Обработка функции очистки данных
@dp.message_handler(commands=['delete'])
async def delete_data(msg: types.Message):
    global last_send_message
    db = sqlite3.connect(f"./users/{msg.from_user.id}.db")
    cur = db.cursor()
    res1 = cur.execute("SELECT film_id FROM history").fetchall()
    res2 = cur.execute("SELECT film_id FROM favorit").fetchall()
    res3 = cur.execute("SELECT film_id FROM viewed").fetchall()
    text1 = '☑️ История пустая' if not res1 else '🔲 История'
    text2 = '☑️ Избранные пустые' if not res2 else '🔲 Избранные'
    text3 = '☑️ Просмотренные пустые' if not res3 else '🔲 Просмотренные'
    db.commit()
    db.close()
    kb1 = [[InlineKeyboardButton(text=text1, callback_data="delete_database_history"),
            InlineKeyboardButton(text=text2, callback_data="delete_database_favorit")],
           [InlineKeyboardButton(text="❌ Меню", callback_data="main_menu2"),
            InlineKeyboardButton(text=text3, callback_data="delete_database_viewed")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb1)
    if msg.photo:
        await last_send_message.delete()
        last_send_message = await msg.answer(text="Выбор разделов очистки",reply_markup=keyboard)
    else:
        await mc.delete_message(bot, msg.from_user.id, msg.message_id)
        last_send_message = await last_send_message.edit_text(text="Выбор разделов очистки", reply_markup=keyboard)
@dp.callback_query_handler(lambda c: c.data.startswith("delete_database"))
async def random_action(call: types.CallbackQuery):
    global last_send_message
    item = call.data.split("_")
    Item = item[2].lower()
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    res1 = cur.execute("SELECT film_id FROM history").fetchall()
    res2 = cur.execute("SELECT film_id FROM favorit").fetchall()
    res3 = cur.execute("SELECT film_id FROM viewed").fetchall()
    text1 = '☑️ История пустая' if not res1 else '🔲 История'
    text2 = '☑️ Избранные пустые' if not res2 else '🔲 Избранные'
    text3 = '☑️ Просмотренные пустые' if not res3 else '🔲 Просмотренные'
    if Item == 'history':
        try:
            cur.execute("DELETE FROM history")
            db.commit()
            text1 = "☑️ История пустая"
        except:
            pass
    elif Item == 'favorit':
        try:
            cur.execute("DELETE FROM favorit")
            db.commit()
            text2 = '☑️ Избранные пустые'
        except:
            pass
    elif Item == 'viewed':
        try:
            cur.execute("DELETE FROM viewed")
            db.commit()
            text3 = '☑️ Просмотренные пустые'
        except:
            pass
    db.close()
    kb1 = [[InlineKeyboardButton(text=text1, callback_data="delete_database_history"),
            InlineKeyboardButton(text=text2, callback_data="delete_database_favorit")],
           [InlineKeyboardButton(text="❌ Меню", callback_data="main_menu2"),
            InlineKeyboardButton(text=text3, callback_data="delete_database_viewed")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb1)
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text="Выбор разделов очистки", reply_markup=keyboard)
    else:
        last_send_message = await last_send_message.edit_text(text="Выбор разделов очистки", reply_markup=keyboard)





































#Обработка функции Подбор
@dp.callback_query_handler(text="random_value")
async def random_value(call: types.CallbackQuery):
    global last_send_message, viewed_message, history_id, index
    viewed_message = []
    history_id = []
    index = 1

    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(tx.KB_RANDOM_TEXT.header.format(name=call.message.from_user.full_name),
                                                  reply_markup=kb.menu_kb4)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_RANDOM_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb4)
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    cur.execute("DELETE FROM last_films")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
# Выбор жанра
@dp.callback_query_handler(text="random_genre")
async def random_genre(call: types.CallbackQuery):
    global last_send_message, viewed_message, history_id, index
    viewed_message = []
    history_id = []
    index = 1
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(tx.KB_RANDOM_GENRE1_TEXT.header.format(name=call.message.from_user.full_name),
                              reply_markup=kb.menu_kb5)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_RANDOM_GENRE1_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb5)
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    cur.execute("DELETE FROM last_films")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="random_two")
async def random_two(call: types.CallbackQuery):
    global last_send_message, viewed_message, history_id, index
    viewed_message = []
    history_id = []
    index = 1
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(
            tx.KB_RANDOM_GENRE2_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb6)
    else:
        last_send_message = await call.message.edit_text(tx.KB_RANDOM_GENRE2_TEXT.header.format(name=call.message.from_user.full_name),
                              reply_markup=kb.menu_kb6)
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    cur.execute("DELETE FROM last_films")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(lambda c: c.data.startswith("genre_select")) #genre_select_fantastuc
async def random_action(call: types.CallbackQuery):
    global last_send_message, history, viewed_message, Genre, history_id, index
    index = 1
    dop_genre = ['вестерн', 'криминал', 'фентэзи', 'ужасы', 'мелодрама', 'военный']
    genre = call.data.split("_")  # Получаем жанр из callback-данных ['genre, 'select, 'боевик]
    Genre = genre[2].lower()  # Приводим жанр к нижнему регистру
    if Genre == 'боевик':
        results = mc.search_film_genre(genre=Genre)
        results2 = mc.search_film_genre(genre=dop_genre[0])
        for item in results2:
            results.append(item)
    elif Genre == 'детектив':
        results = mc.search_film_genre(genre=Genre)
        results2 = mc.search_film_genre(genre=dop_genre[1])
        for item in results2:
            results.append(item)
    elif Genre == 'фантастика':
        results = mc.search_film_genre(genre=Genre)
        results2 = mc.search_film_genre(genre=dop_genre[2])
        for item in results2:
            results.append(item)
    elif Genre == 'триллер':
        results = mc.search_film_genre(genre=Genre)
        results2 = mc.search_film_genre(genre=dop_genre[3])
        for item in results2:
            results.append(item)
    elif Genre == 'драма':
        results = mc.search_film_genre(genre=Genre)
        results2 = mc.search_film_genre(genre=dop_genre[4])
        for item in results2:
            results.append(item)
    elif Genre == 'история':
        results = mc.search_film_genre(genre=Genre)
        results2 = mc.search_film_genre(genre=dop_genre[5])
        for item in results2:
            results.append(item)
    else:
        results = mc.search_film_genre(genre=Genre)

    while True:
        film_id_choice = random.choice(results)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(results):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Genre_Select - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="next_film_genre")
async def next_films(call: types.CallbackQuery):
    global Genre
    await random_action2(call=call, genre=Genre)
async def random_action2(call: types.CallbackQuery, genre: str):
    global last_send_message, history, viewed_message, history_id, index
    index = 1
    genre_lower = genre.lower()
    dop_genre = ['вестерн', 'криминал', 'фентэзи', 'ужасы', 'мелодрама', 'военный']
    if genre_lower == 'боевик':
        results = mc.search_film_genre(genre=genre_lower)
        results2 = mc.search_film_genre(genre=dop_genre[0])
        for item in results2:
            results.append(item)
    elif genre_lower == 'детектив':
        results = mc.search_film_genre(genre=genre_lower)
        results2 = mc.search_film_genre(genre=dop_genre[1])
        for item in results2:
            results.append(item)
    elif genre_lower == 'фантастика':
        results = mc.search_film_genre(genre=genre_lower)
        results2 = mc.search_film_genre(genre=dop_genre[2])
        for item in results2:
            results.append(item)
    elif genre_lower == 'триллер':
        results = mc.search_film_genre(genre=genre_lower)
        results2 = mc.search_film_genre(genre=dop_genre[3])
        for item in results2:
            results.append(item)
    elif genre_lower == 'драма':
        results = mc.search_film_genre(genre=genre_lower)
        results2 = mc.search_film_genre(genre=dop_genre[4])
        for item in results2:
            results.append(item)
    elif genre_lower == 'история':
        results = mc.search_film_genre(genre=genre_lower)
        results2 = mc.search_film_genre(genre=dop_genre[5])
        for item in results2:
            results.append(item)
    else:
        results = mc.search_film_genre(genre=genre_lower)

    while True:
        film_id_choice = random.choice(results)
        if film_id_choice not in viewed_message and (not history or film_id_choice != history[-1]):
            break
        elif len(viewed_message) == len(results):
            viewed_message = []
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    media = InputMediaPhoto(info[6], caption=text)
    print(f"Next_Film_Genre - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(lambda c: c.data.startswith("back_film_genre"))
async def random_action(call: types.CallbackQuery):
    global history_id, index, last_send_message

    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_id FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])

    index += 1
    if index > len(result):
        return False
    iter = len(result) - index
    info = mc.select_film_info(result[iter])
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {result[iter]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Back_Film_Genre - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (result[iter],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="add_favorit_genre")
async def add_favorit(call: types.CallbackQuery):
    global index
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    info = mc.select_film_info(film_id[0])
    film_name = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if film_name == None:
        cur.execute("INSERT INTO favorit VALUES (?, ?, ?)", (data, film_id[0], info[1]))
        print(f"Добавлено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    else:
        cur.execute("DELETE FROM favorit WHERE film_id = ?", (film_id[0],))
        print(f"Удалено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard)
@dp.callback_query_handler(text="more_genre")
async def more_genre(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"More_Genre - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[10] != 'None':
        buttons.append(InlineKeyboardButton('Kinopoisk', url=info[10]))
    else:
        buttons.append(InlineKeyboardButton(''))
    if info[13] != 'None':
        buttons.append(InlineKeyboardButton('WikiPedia', url=info[13]))
    else:
        buttons.append(InlineKeyboardButton(''))
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(
        InlineKeyboardButton('❌ Назад', callback_data='more_genre_back'),
        InlineKeyboardButton('🎥 Ссылки', callback_data='url_genre'))
    text = f"{info[1]}\n\nОписание: {info[7]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    db.commit()
    db.close()
@dp.callback_query_handler(text="more_genre_back")
async def more_genre_back(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    viewed_message.append(film_id[0])
    history.append(film_id[0])
    info = mc.select_film_info(film_id[0])
    history_id.append(film_id[0])
    if info[6][0:6:1] != 'https:': info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id[0]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"More_Genre_Back - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_genre")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_genre")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="url_genre")
async def url_genre(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"Url_Genre - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[11] != 'None':
        buttons.append(InlineKeyboardButton('SerialFan', url=info[11]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[12] != 'None':
        buttons.append(InlineKeyboardButton('LordFilm', url=info[12]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[14] != 'None':
        buttons.append(InlineKeyboardButton('ZetFlix', url=info[14]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[15] != 'None':
        buttons.append(InlineKeyboardButton('Tvigle', url=info[15]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[16] != 'None':
        buttons.append(InlineKeyboardButton('KinopoiskHD', url=info[16]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[17] != 'None':
        buttons.append(InlineKeyboardButton('MultOnline', url=info[17]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))

    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('❌ Назад', callback_data='more_genre'))
    text = f"{info[1]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    cur.execute("INSERT INTO viewed VALUES (?, ?, ?)", (data, film_id[0], info[1]))
    db.commit()
    db.close()
# Выбор страны
@dp.callback_query_handler(text="random_country")
async def random_two(call: types.CallbackQuery):
    global last_send_message, viewed_message, history_id, index
    viewed_message = []
    history_id = []
    index = 1
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(
            tx.KB_RANDOM_COUNTRY_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb8)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_RANDOM_COUNTRY_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb8)
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    cur.execute("DELETE FROM last_films")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(lambda c: c.data.startswith("country_select"))
async def random_action(call: types.CallbackQuery):
    global last_send_message, history, viewed_message, Country, history_id, index
    index = 1
    country = call.data.split("_")
    Country = country[2].lower()
    if Country == 'сша' or Country == 'ссср':
        Country = Country.upper()
    else:
        Country = Country[0].upper() + Country[1::1]
    if Country == 'Россия':
        result = mc.search_film_country(Country)
        result2 = mc.search_film_country('СССР')
        for item in result2:
            result.append(item)
    elif Country == 'Англия':
        result = mc.search_film_country('Великобритания')
    elif Country == 'Корея':
        result = mc.search_film_country('Корея Южная')
    else:
        result = mc.search_film_country(Country)
    while True:
        film_id_choice = random.choice(result)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(result):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Country_Select - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="next_film_country")
async def next_films(call: types.CallbackQuery):
    global Country
    await random_action3(call=call, country=Country)
async def random_action3(call: types.CallbackQuery, country: str):
    global last_send_message, history, viewed_message, history_id, index
    index = 1
    if country == 'сша' or Country == 'ссср':
        country = country.upper()
    else:
        country = country[0].upper() + country[1::1]
    if country == 'Россия':
        result = mc.search_film_country(country)
        result2 = mc.search_film_country('СССР')
        for item in result2:
            result.append(item)
    elif country == 'Англия':
        result = mc.search_film_country('Великобритания')
    elif country == 'Корея':
        result = mc.search_film_country('Корея Южная')
    else:
        result = mc.search_film_country(country)
    while True:
        film_id_choice = random.choice(result)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(result):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Next_Film_Country - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(lambda c: c.data.startswith("back_film_country"))
async def random_action(call: types.CallbackQuery):
    global history_id, index, last_send_message

    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_id FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    index += 1
    if index > len(result):
        return False
    iter = len(result) - index
    info = mc.select_film_info(result[iter])
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {result[iter]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Back_Film_Country - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (result[iter],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="add_favorit_country")
async def add_favorit(call: types.CallbackQuery):
    global index
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    info = mc.select_film_info(film_id[0])
    film_name = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if film_name == None:
        cur.execute("INSERT INTO favorit VALUES (?, ?, ?)", (data, film_id[0], info[1]))
        print(f"Добавлено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    else:
        cur.execute("DELETE FROM favorit WHERE film_id = ?", (film_id[0],))
        print(f"Удалено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard)

@dp.callback_query_handler(text="more_country")
async def more_country(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"More_Country_Back - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[10] != 'None':
        buttons.append(InlineKeyboardButton('Kinopoisk', url=info[10]))
    else:
        buttons.append(InlineKeyboardButton(''))
    if info[13] != 'None':
        buttons.append(InlineKeyboardButton('WikiPedia', url=info[13]))
    else:
        buttons.append(InlineKeyboardButton(''))
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(
        InlineKeyboardButton('❌ Назад', callback_data='more_country_back'),
        InlineKeyboardButton('🎥 Ссылки', callback_data='url_country'))
    text = f"{info[1]}\n\nОписание: {info[7]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    db.commit()
    db.close()
@dp.callback_query_handler(text="more_country_back")
async def more_country_back(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    viewed_message.append(film_id[0])
    history.append(film_id[0])
    info = mc.select_film_info(film_id[0])
    history_id.append(film_id[0])
    if info[6][0:6:1] != 'https:': info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id[0]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"More_Country_Back - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_country")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_country")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="url_country")
async def url_country(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"Url_Country - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[11] != 'None':
        buttons.append(InlineKeyboardButton('SerialFan', url=info[11]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[12] != 'None':
        buttons.append(InlineKeyboardButton('LordFilm', url=info[12]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[14] != 'None':
        buttons.append(InlineKeyboardButton('ZetFlix', url=info[14]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[15] != 'None':
        buttons.append(InlineKeyboardButton('Tvigle', url=info[15]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[16] != 'None':
        buttons.append(InlineKeyboardButton('KinopoiskHD', url=info[16]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[17] != 'None':
        buttons.append(InlineKeyboardButton('MultOnline', url=info[17]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))

    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('❌ Назад', callback_data='more_country'))
    text = f"{info[1]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    cur.execute("INSERT INTO viewed VALUES (?, ?, ?)", (data, film_id[0], info[1]))
    db.commit()
    db.close()
# Выбор года
@dp.callback_query_handler(text="random_year")
async def random_two(call: types.CallbackQuery):
    global last_send_message, viewed_message, history_id, index
    viewed_message = []
    history_id = []
    index = 1
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(
            tx.KB_RANDOM_YEAR.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb10)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_RANDOM_YEAR.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb10)
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    cur.execute("DELETE FROM last_films")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(lambda c: c.data.startswith("year_select"))
async def random_action(call: types.CallbackQuery):
    global last_send_message, history, viewed_message, Year, history_id, index
    index = 1
    year = call.data.split("_")
    Year = year[2].lower()
    if Year == '2020':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 2020 AND film_year <= 2029 ORDER BY film_year"
    elif Year == '2010':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 2010 AND film_year <= 2019 ORDER BY film_year"
    elif Year == '2000':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 2000 AND film_year <= 2009 ORDER BY film_year"
    elif Year == '1990':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 1990 AND film_year <= 1999 ORDER BY film_year"
    elif Year == '1980':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 1980 AND film_year <= 1989 ORDER BY film_year"
    elif Year == '1970':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 1970 AND film_year <= 1979 ORDER BY film_year"
    else:
        return False
    films = film_cur.execute(text_bd).fetchall()
    film_id = []
    for item in films:
        film_id.append(item[0])
    while True:
        film_id_choice = random.choice(film_id)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(film_id):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Year_Select - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="next_film_year")
async def next_films(call: types.CallbackQuery):
    global Year
    await random_action4(call=call, year=Year)
async def random_action4(call: types.CallbackQuery, year: str):
    global last_send_message, history, viewed_message, history_id, index
    index = 1
    if year == '2020':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 2020 AND film_year <= 2029 ORDER BY film_year"
    elif year == '2010':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 2010 AND film_year <= 2019 ORDER BY film_year"
    elif year == '2000':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 2000 AND film_year <= 2009 ORDER BY film_year"
    elif year == '1990':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 1990 AND film_year <= 1999 ORDER BY film_year"
    elif year == '1980':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 1980 AND film_year <= 1989 ORDER BY film_year"
    elif year == '1970':
        text_bd = "SELECT film_id FROM database WHERE film_year >= 1970 AND film_year <= 1979 ORDER BY film_year"
    else:
        return False
    films = film_cur.execute(text_bd).fetchall()
    film_id = []
    for item in films:
        film_id.append(item[0])
    while True:
        film_id_choice = random.choice(film_id)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(film_id):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Next_Film_Year - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()

@dp.callback_query_handler(lambda c: c.data.startswith("back_film_year"))
async def random_action(call: types.CallbackQuery):
    global history_id, index, last_send_message

    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_id FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    index += 1
    if index > len(result):
        return False
    iter = len(result) - index
    info = mc.select_film_info(result[iter])
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {result[iter]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Back_Film_Year - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (result[iter],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)

    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="add_favorit_year")
async def add_favorit(call: types.CallbackQuery):
    global index
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    info = mc.select_film_info(film_id[0])
    film_name = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if film_name == None:
        cur.execute("INSERT INTO favorit VALUES (?, ?, ?)", (data, film_id[0], info[1]))
        print(f"Добавлено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    else:
        cur.execute("DELETE FROM favorit WHERE film_id = ?", (film_id[0],))
        print(f"Удалено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=keyboard)
@dp.callback_query_handler(text="more_year")
async def more_year(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"More_Year - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[10] != 'None':
        buttons.append(InlineKeyboardButton('Kinopoisk', url=info[10]))
    else:
        buttons.append(InlineKeyboardButton(''))
    if info[13] != 'None':
        buttons.append(InlineKeyboardButton('WikiPedia', url=info[13]))
    else:
        buttons.append(InlineKeyboardButton(''))
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(
        InlineKeyboardButton('❌ Назад', callback_data='more_year_back'),
        InlineKeyboardButton('🎥 Ссылки', callback_data='url_year'))
    text = f"{info[1]}\n\nОписание: {info[7]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    db.commit()
    db.close()
@dp.callback_query_handler(text="more_year_back")
async def more_year_back(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    viewed_message.append(film_id[0])
    history.append(film_id[0])
    info = mc.select_film_info(film_id[0])
    history_id.append(film_id[0])
    if info[6][0:6:1] != 'https:': info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id[0]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"More_Year_Back - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_year")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_year")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="url_year")
async def url_year(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"Url_Year - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[11] != 'None':
        buttons.append(InlineKeyboardButton('SerialFan', url=info[11]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[12] != 'None':
        buttons.append(InlineKeyboardButton('LordFilm', url=info[12]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[14] != 'None':
        buttons.append(InlineKeyboardButton('ZetFlix', url=info[14]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[15] != 'None':
        buttons.append(InlineKeyboardButton('Tvigle', url=info[15]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[16] != 'None':
        buttons.append(InlineKeyboardButton('KinopoiskHD', url=info[16]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[17] != 'None':
        buttons.append(InlineKeyboardButton('MultOnline', url=info[17]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))

    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('❌ Назад', callback_data='more_year'))
    text = f"{info[1]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    cur.execute("INSERT INTO viewed VALUES (?, ?, ?)", (data, film_id[0], info[1]))
    db.commit()
    db.close()
# Выбор Рейтинга
@dp.callback_query_handler(text="random_rating")
async def random_two(call: types.CallbackQuery):
    global last_send_message, viewed_message, history_id, index
    viewed_message = []
    history_id = []
    index = 1
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(
            tx.KB_RANDOM_RATING.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb12)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_RANDOM_RATING.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb12)
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    cur.execute("DELETE FROM last_films")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(lambda c: c.data.startswith("rating_select"))
async def random_action(call: types.CallbackQuery):
    global last_send_message, history, viewed_message, Rating, history_id, index
    index = 1
    rating = call.data.split("_")
    Rating = rating[2].lower()
    if Rating == '6':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '6.0' AND film_rating <= '6.9' ORDER BY film_rating"
    elif Rating == '7':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '7.0' AND film_rating <= '7.9' ORDER BY film_rating"
    elif Rating == '8':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '8.0' AND film_rating <= '8.9' ORDER BY film_rating"
    elif Rating == '9':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '9.0' AND film_rating <= '9.9' ORDER BY film_rating"
    else:
        return False
    films = film_cur.execute(text_bd).fetchall()
    film_id = []
    for item in films:
        film_id.append(item[0])
    while True:
        film_id_choice = random.choice(film_id)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(film_id):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Rating_Select - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice, )).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)

    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="next_film_rating")
async def next_films(call: types.CallbackQuery):
    global Rating
    await random_action5(call=call, rating=Rating)
async def random_action5(call: types.CallbackQuery, rating: str):
    global last_send_message, history, viewed_message, history_id, index
    index = 1
    if rating == '6':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '6.0' AND film_rating <= '6.9' ORDER BY film_rating"
    elif rating == '7':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '7.0' AND film_rating <= '7.9' ORDER BY film_rating"
    elif rating == '8':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '8.0' AND film_rating <= '8.9' ORDER BY film_rating"
    elif rating == '9':
        text_bd = "SELECT film_id FROM filminfo WHERE film_rating >= '9.0' AND film_rating <= '9.9' ORDER BY film_rating"
    else:
        return False
    films = film_cur.execute(text_bd).fetchall()
    film_id = []
    for item in films:
        film_id.append(item[0])
    while True:
        film_id_choice = random.choice(film_id)
        if film_id_choice not in viewed_message:
            if not history:
                break
            else:
                if film_id_choice == history[-1]:
                    continue
                else:
                    break
        elif len(viewed_message) == len(film_id):
            viewed_message = []
            continue
        else:
            continue
    viewed_message.append(film_id_choice)
    history.append(film_id_choice)
    info = mc.select_film_info(film_id_choice)
    history_id.append(film_id_choice)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id_choice}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Next_Film_Rating - {info[1]}")
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id_choice,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("INSERT INTO history VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("INSERT INTO last_films VALUES (?, ?)", (film_id_choice, info[1]))
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()

@dp.callback_query_handler(lambda c: c.data.startswith("back_film_rating"))
async def random_action(call: types.CallbackQuery):
    global history_id, index, last_send_message

    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_id FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    index += 1
    if index > len(result):
        return False
    iter = len(result) - index
    info = mc.select_film_info(result[iter])
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {result[iter]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"Back_Film_rating - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (result[iter],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="add_favorit_rating")
async def add_favorit(call: types.CallbackQuery):
    global index
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    info = mc.select_film_info(film_id[0])
    film_name = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if film_name == None:
        cur.execute("INSERT INTO favorit VALUES (?, ?, ?)", (data, film_id[0], info[1]))
        print(f"Добавлено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
             InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
            [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
             InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_rating")],
            [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    else:
        cur.execute("DELETE FROM favorit WHERE film_id = ?", (film_id[0],))
        print(f"Удалено - {data} {info[1]} {film_id[0]}")
        db.commit()
        db.close()
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=keyboard)
@dp.callback_query_handler(text="more_rating")
async def more_rating(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"More_Rating - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[10] != 'None':
        buttons.append(InlineKeyboardButton('Kinopoisk', url=info[10]))
    else:
        buttons.append(InlineKeyboardButton(''))
    if info[13] != 'None':
        buttons.append(InlineKeyboardButton('WikiPedia', url=info[13]))
    else:
        buttons.append(InlineKeyboardButton(''))
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(
        InlineKeyboardButton('❌ Назад', callback_data='more_rating_back'),
        InlineKeyboardButton('🎥 Ссылки', callback_data='url_rating'))
    text = f"{info[1]}\n\nОписание: {info[7]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    db.commit()
    db.close()
@dp.callback_query_handler(text="more_rating_back")
async def more_rating_back(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    viewed_message.append(film_id[0])
    history.append(film_id[0])
    info = mc.select_film_info(film_id[0])
    history_id.append(film_id[0])
    if info[6][0:6:1] != 'https:': info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id[0]}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    print(f"More_Rating_Back - {info[1]}")
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id[0],)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    else:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
                 InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_rating")],
                [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_rating")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(info[6], caption=text),
                                                         reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': text
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="url_rating")
async def url_rating(call: types.CallbackQuery):
    global last_send_message
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM last_films").fetchall()
    result = []
    for item in results:
        result.append(item[0])
    ind = len(result) - index
    print(f"Url_Rating - {result[ind]}")
    film_id = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (result[ind],)).fetchone()
    info = mc.select_film_info(film_id[0])
    buttons = []
    if info[11] != 'None':
        buttons.append(InlineKeyboardButton('SerialFan', url=info[11]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[12] != 'None':
        buttons.append(InlineKeyboardButton('LordFilm', url=info[12]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[14] != 'None':
        buttons.append(InlineKeyboardButton('ZetFlix', url=info[14]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[15] != 'None':
        buttons.append(InlineKeyboardButton('Tvigle', url=info[15]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[16] != 'None':
        buttons.append(InlineKeyboardButton('KinopoiskHD', url=info[16]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[17] != 'None':
        buttons.append(InlineKeyboardButton('MultOnline', url=info[17]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))

    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('❌ Назад', callback_data='more_rating'))
    text = f"{info[1]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    cur.execute("INSERT INTO viewed VALUES (?, ?, ?)", (data, film_id[0], info[1]))
    db.commit()
    db.close()





















# Обработка функции Поиск
class SearchState(StatesGroup):
    MODE = State()
    NAME = State()
    ID = State()
@dp.callback_query_handler(text="search_films")
async def search_films(call: types.CallbackQuery, state=SearchState.MODE):
    global last_send_message
    kb13 = [[InlineKeyboardButton(text="По названию", callback_data="search_films_name"),
             InlineKeyboardButton(text="По ID", callback_data="search_films_id")],
            [InlineKeyboardButton(text="❌ Назад", callback_data="main_menu")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await SearchState.MODE.set()
    async with state.proxy() as data:
        data['search_mode'] = True
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text="📌 Выберите критерий поиска", reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text(text="📌 Выберите критерий поиска", reply_markup=keyboard)
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="search_films_2", state="*")
async def search_films(call: types.CallbackQuery, state=SearchState.MODE):
    global last_send_message
    kb13 = [[InlineKeyboardButton(text="По названию", callback_data="search_films_name"),
             InlineKeyboardButton(text="По ID", callback_data="search_films_id")],
            [InlineKeyboardButton(text="❌ Назад", callback_data="main_menu")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await SearchState.MODE.set()
    async with state.proxy() as data:
        data['search_mode'] = True
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text="📌 Выберите критерий поиска", reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text(text="📌 Выберите критерий поиска", reply_markup=keyboard)
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.callback_query_handler(text="search_films_name", state=SearchState.MODE)
@dp.callback_query_handler(text="search_films_id", state=SearchState.MODE)
async def handle_search_mode(call: types.CallbackQuery, state: SearchState.MODE):
    global last_send_message, Search
    async with state.proxy() as data:
        kb13 = [[InlineKeyboardButton(text="❌ Назад", callback_data="search_films_2")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
        if data.get('search_mode'):
            search_mode = call.data
            if search_mode == "search_films_name":
                await SearchState.NAME.set()
                Search = 'NAME'
                text = "Введите имя фильма"
            elif search_mode == "search_films_id":
                await SearchState.ID.set()
                Search = 'ID'
                text = "Введите ID фильма"
            if call.message.photo:
                await last_send_message.delete()
                last_send_message = await call.message.answer(text=text, reply_markup=keyboard)
            else:
                last_send_message = await call.message.edit_text(text=text, reply_markup=keyboard)
        else:
            print('NO - Search_FILMS')
            return False
@dp.message_handler(lambda message: not message.text.isdigit(), state=SearchState.ID)
async def process_id_input_invalid(message: types.Message):
    global last_send_message
    kb13 = [[InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    await mc.delete_message(bot, message.from_user.id, message.message_id)
    last_send_message = await last_send_message.edit_text(text="Пожалуйста, введите корректный ID фильма (число)",
                                                reply_markup=keyboard)
@dp.message_handler(state=SearchState.NAME)
@dp.message_handler(lambda message: message.text.isdigit(), state=SearchState.ID)
async def process_id_input_valid(message: types.Message, state: SearchState.NAME):
    await print_film_search(message, state)
async def print_film_search(message: types.Message, state: SearchState.NAME):
    global last_send_message, last_film, Search
    async with state.proxy() as data:
        if Search == 'NAME':
            data['film_name'] = message.text
            film_name = data.get('film_name')
            result = film_cur.execute("SELECT film_id FROM database WHERE film_name = ?", (film_name,)).fetchone()
            if result is None:
                film_id = film_name
            else:
                film_id = result[0]
        elif Search == 'ID':
            data['film_id'] = int(message.text)
            film_id = data.get('film_id')
            result = film_cur.execute("SELECT film_id FROM database WHERE film_id = ?", (film_id,)).fetchone()
    await mc.delete_message(bot, message.from_user.id, message.message_id)
    if result == None:
        kb13 = [[InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
        last_send_message = await last_send_message.edit_text(text=f"Фильм {film_id} не найден", reply_markup=keyboard)
    else:
        info = mc.select_film_info(film_id)
        last_film.append(film_id)
        if info[6][0:6:1] != 'https:':
            info[6] = 'https:' + info[6]
        text = f"{info[1]}\n\nID: {film_id}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
               f"Длительность: {info[5]}"
        db = sqlite3.connect(f'./users/{message.from_user.id}.db')
        cur = db.cursor()
        results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id,)).fetchone()
        if results == None:
            kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_search"),
                     InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_search")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
        else:
            kb13 = [[InlineKeyboardButton(text="❤️ В избранном", callback_data="add_favorit_search"),
                     InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_search")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
        if message.photo:
            last_send_message = await bot.edit_message_media(chat_id=message.chat.id,
                                                                           message_id=message.message_id,
                                                                           media=InputMediaPhoto(info[6], caption=text),
                                                                           reply_markup=keyboard)
        else:
            await last_send_message.delete()
            last_send_message = await bot.send_photo(chat_id=message.chat.id, photo=info[6], caption=text,
                                                     reply_markup=keyboard)
    await state.finish()
@dp.callback_query_handler(text="print_film_search2")
async def print_film_search2(call: types.CallbackQuery):
    global last_send_message, last_film, Search
    film_id = last_film[len(last_film) - 1]
    info = mc.select_film_info(film_id)
    last_film.append(film_id)
    if info[6][0:6:1] != 'https:':
        info[6] = 'https:' + info[6]
    text = f"{info[1]}\n\nID: {film_id}\nЖанр: {info[2]}\nГод: {info[3]}\nРейтинг: {info[8]}\nСтрана: {info[9]}\n" \
           f"Длительность: {info[5]}"
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (film_id,)).fetchone()
    if results == None:
        kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_search"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_search")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
    else:
        kb13 = [[InlineKeyboardButton(text="❤️ В избранном", callback_data="add_favorit_search"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_search")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb13)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                                       message_id=call.message.message_id,
                                                                       media=InputMediaPhoto(info[6], caption=text),
                                                                       reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
@dp.callback_query_handler(text="more_search")
async def more_search(call: types.CallbackQuery):
    global last_send_message, last_film
    info = mc.select_film_info(last_film[len(last_film) - 1])
    buttons = []
    if info[10] != 'None':
        buttons.append(InlineKeyboardButton('Kinopoisk', url=info[10]))
    else:
        buttons.append(InlineKeyboardButton(''))
    if info[13] != 'None':
        buttons.append(InlineKeyboardButton('WikiPedia', url=info[13]))
    else:
        buttons.append(InlineKeyboardButton(''))
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(
        InlineKeyboardButton('❌ Назад', callback_data='print_film_search2'),
        InlineKeyboardButton('🎥 Ссылки', callback_data='url_search'))
    text = f"{info[1]}\n\nОписание: {info[7]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
@dp.callback_query_handler(text="url_search")
async def url_search(call: types.CallbackQuery):
    global last_send_message, last_film
    info = mc.select_film_info(last_film[len(last_film) - 1])
    buttons = []
    if info[11] != 'None':
        buttons.append(InlineKeyboardButton('SerialFan', url=info[11]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[12] != 'None':
        buttons.append(InlineKeyboardButton('LordFilm', url=info[12]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[14] != 'None':
        buttons.append(InlineKeyboardButton('ZetFlix', url=info[14]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[15] != 'None':
        buttons.append(InlineKeyboardButton('Tvigle', url=info[15]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[16] != 'None':
        buttons.append(InlineKeyboardButton('KinopoiskHD', url=info[16]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    if info[17] != 'None':
        buttons.append(InlineKeyboardButton('MultOnline', url=info[17]))
    else:
        buttons.append(InlineKeyboardButton('', callback_data='empty_button_pressed'))
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.insert(button)
    keyboard.row(InlineKeyboardButton('❌ Назад', callback_data='more_search'))
    text = f"{info[1]}"
    info[6] = 'https:' + info[6] if not info[6].startswith('https:') else info[6]
    media = InputMediaPhoto(info[6], caption=text)
    if call.message.photo:
        last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=media, reply_markup=keyboard)
    else:
        await last_send_message.delete()
        last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=info[6], caption=text,
                                                 reply_markup=keyboard)
@dp.callback_query_handler(text="add_favorit_search")
async def add_favorit(call: types.CallbackQuery):
    global last_send_message, last_film
    buttons  = []
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    info = mc.select_film_info(last_film[len(last_film) - 1])
    current_datetime = datetime.datetime.now()
    data = current_datetime.strftime("%d:%m:%Y - %H:%M")
    film_name = cur.execute("SELECT film_name FROM favorit WHERE film_id = ?", (last_film[0],)).fetchone()
    if film_name == None:
        cur.execute("INSERT INTO favorit VALUES (?, ?, ?)", (data, last_film[0], info[1]))
        print(f"Добавлено - {data} {info[1]} {last_film[0]}")
        db.commit()
        db.close()
        keyboard = [[InlineKeyboardButton(text='❤️ В избранном', callback_data="add_favorit_search"),
                     InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_search")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
    else:
        cur.execute("DELETE FROM favorit WHERE film_id = ?", (last_film[0],))
        print(f"Удалено - {data} {info[1]} {last_film[0]}")
        db.commit()
        db.close()
        keyboard = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit_search"),
                 InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="more_search")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="search_films")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=keyboard)











#Обработка Callback-вызовов в меню Развлечения
@dp.callback_query_handler(text="generation_film")
async def generation_film(call: types.CallbackQuery):
    global last_send_message, last_generate
    last_generate = []
    keyboard = [[InlineKeyboardButton(text="🐱 Коты", callback_data="generate_api_cats"),
                 InlineKeyboardButton(text="🦆 Утки", callback_data="generate_api_duck")],
                [InlineKeyboardButton(text="💼 Занятия", callback_data="generate_api_work"),
                 InlineKeyboardButton(text="😂 Шутки", callback_data="generate_api_jok")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="main_menu2")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text="📌 Выберите что сгенерировать",
                              reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text(text="📌 Выберите что сгенерировать",
            reply_markup=keyboard)
@dp.callback_query_handler(lambda c: c.data.startswith("generate_api"))
async def generate_api(call: types.CallbackQuery):
    global last_send_message, last_generate
    api = call.data.split("_")
    API = api[2].lower()

    if API == 'cats':
        keyboard = [[InlineKeyboardButton(text="🔄 Еще", callback_data="generate_api_cats")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="generation_film")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        while True:
            text = await mc.cat2()
            if text not in last_generate:
                last_generate.append(text)
                break
        await mc.cat3()
        if text == None:
            return False
        input_photo = "cat_image.jpg"
        if call.message.photo:
            last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                         message_id=call.message.message_id,
                                                         media=InputMediaPhoto(InputFile(input_photo), caption=text),
                                                         reply_markup=keyboard)
        else:
            await last_send_message.delete()
            last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile(input_photo), caption=text,
                                                     reply_markup=keyboard)
    elif API == 'duck':
        keyboard = [[InlineKeyboardButton(text="🔄 Еще", callback_data="generate_api_duck")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="generation_film")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        while True:
            photo = mc.duck()
            if photo not in last_generate:
                last_generate.append(photo)
                break
        if photo == None:
            return False
        if call.message.photo:
            last_send_message = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                             message_id=call.message.message_id,
                                                             media=InputMediaPhoto(photo),
                                                             reply_markup=keyboard)
        else:
            await last_send_message.delete()
            last_send_message = await bot.send_photo(chat_id=call.message.chat.id, photo=photo,
                                                     reply_markup=keyboard)
    elif API == 'jok':
        keyboard = [[InlineKeyboardButton(text="🔄 Еще", callback_data="generate_api_jok")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="generation_film")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        while True:
            text = mc.jok()
            if text not in last_generate:
                last_generate.append(text)
                break
        if text == None:
            return False
        if call.message.photo:
            await last_send_message.delete()
            last_send_message = await call.answer(text, reply_markup=keyboard)
        else:
            last_send_message = await last_send_message.edit_text(text=text, reply_markup=keyboard)
    elif API == 'work':
        keyboard = [[InlineKeyboardButton(text="🔄 Еще", callback_data="generate_api_work")],
                    [InlineKeyboardButton(text="❌ Назад", callback_data="generation_film")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        while True:
            text = mc.work()
            if text not in last_generate:
                last_generate.append(text)
                break
        if text == None:
            return False
        if call.message.photo:
            await last_send_message.delete()
            last_send_message = await call.answer(text, reply_markup=keyboard)
        else:
            last_send_message = await last_send_message.edit_text(text=text, reply_markup=keyboard)
    else:
        return False









#Обработка вызовов в меню Заказ
class BuyFilm(StatesGroup):
    MODE = State()
@dp.callback_query_handler(text="buy_films")
async def buy_films(call: types.CallbackQuery, state=BuyFilm.MODE):
    global last_send_message
    keyboard = [[InlineKeyboardButton(text="❌ Назад", callback_data="main_menu3")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await BuyFilm.MODE.set()
    async with state.proxy() as data:
        data['buy_films'] = True
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text="📌 Введите название фильма или ссылку на него", reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text(text="📌 Введите название фильма или ссылку на него", reply_markup=keyboard)
    db = sqlite3.connect(f'./users/{call.from_user.id}.db')
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
@dp.message_handler(state=BuyFilm.MODE)
async def process_film_input(message: types.Message, state: BuyFilm.MODE):
    await film_input(message, state)
async def film_input(message: types.Message, state: SearchState.NAME):
    global last_send_message
    async with state.proxy() as data:
        data['buy_film_input'] = message.text
        film_name = message.text
    await mc.delete_message(bot, message.from_user.id, message.message_id)
    keyboard = [[InlineKeyboardButton(text="❌ Назад", callback_data="main_menu2")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    if message.photo:
        await last_send_message.delete()
        last_send_message = await message.answer(text=f"✅ Фильм '{film_name}' добавлен", reply_markup=keyboard)
    else:
        last_send_message = await last_send_message.edit_text(text=f"✅ Фильм '{film_name}' добавлен", reply_markup=keyboard)
    db = sqlite3.connect(f'./users/{message.from_user.id}.db')
    cur = db.cursor()
    cur.execute("DELETE FROM last_message")
    last_message_info = {
        'chat_id': last_send_message.chat.id,
        'message_id': last_send_message.message_id,
        'text': 'None'
    }
    cur.execute("INSERT INTO last_message (chat_id, message_id, text) VALUES (?, ?, ?)",
                (last_message_info['chat_id'], last_message_info['message_id'], last_message_info['text']))
    db.commit()
    db.close()
    await state.finish()
    db = sqlite3.connect("./upgrade/name-to-add.db")
    cur = db.cursor()
    cur.execute("INSERT INTO film VALUES (?)", (film_name, ))
    db.commit()
    db.close()
    print(f"Заказан фильм - '{film_name}'")













#Обработка вызовов в меню Просмотр
@dp.callback_query_handler(text="vision_films")
async def vision_films(call: types.CallbackQuery):
    global last_send_message, IND
    IND = 0
    keyboard = [[InlineKeyboardButton(text="Все", callback_data="vision_films_print_all"),
                 InlineKeyboardButton(text="Просмотренные", callback_data="vision_films_print_viewed")],
                [InlineKeyboardButton(text="Избранное", callback_data="vision_films_print_favorit"),
                 InlineKeyboardButton(text="История", callback_data="vision_films_print_history")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="main_menu2")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer("📌 Выберите критерий просмотра",
                              reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text( "📌 Выберите критерий просмотра",
            reply_markup=keyboard)
@dp.callback_query_handler(lambda c: c.data.startswith("vision_films_print"))
async def vision_films_print(call: types.CallbackQuery):
    global last_send_message, IND, text_for_send
    IND = 0
    view = call.data.split("_")
    VIEW = view[3].lower()
    db = sqlite3.connect(f"./users/{call.from_user.id}.db")
    cur = db.cursor()
    if VIEW == 'all':
        results2 = film_cur.execute("SELECT film_id, film_name FROM database").fetchall()
        result = []
        for item in results2:
            result.append(f"{item[0]}. {item[1]}")
        text = "\n".join(result)
    elif VIEW == 'viewed' or VIEW == 'favorit' or VIEW == 'history':
        results2 = cur.execute(f"SELECT film_id, film_name FROM {VIEW} ORDER BY rowid DESC").fetchall()
        result = []
        for item in results2:
            result.append(f""
                          f"{item[0]}. {item[1]}")
        text = "\n".join(result)
    else:
        return False
    if len(text) <=  500:
        keyboard = [[InlineKeyboardButton(text="❌ Назад", callback_data="vision_films")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        text_to_send = f"{text}"
        if len(text_to_send) < 5:
            text_to_send = '🧺 Пока что здесь пусто'
        if call.message.photo:
            await last_send_message.delete()
            last_send_message = await call.message.answer(text_to_send, reply_markup=keyboard)
        else:
            last_send_message = await call.message.edit_text(text_to_send, reply_markup=keyboard)
    else:
        lines = text.split("\n")
        lenght = math.ceil(len(text) / 460)
        text_for_send = []
        lines_dubl = []
        for i in range(0, lenght, 1):
            txt = ""
            for line in lines:
                if len(txt) > 460:
                    break
                if line not in lines_dubl:
                    txt = txt + "\n" + line
                    lines_dubl.append(line)
            text_for_send.append(txt)
        keyboard = [[InlineKeyboardButton(text="◀️ Предыдущий", callback_data="back_vision_films"),
                         InlineKeyboardButton(text="▶️ Следующий", callback_data="next_vision_films")],
                        [InlineKeyboardButton(text="❌ Назад", callback_data="vision_films")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        if call.message.photo:
            await last_send_message.delete()
            last_send_message = await call.message.answer(text=text_for_send[IND], reply_markup=keyboard)
        else:
            last_send_message = await call.message.edit_text(text=text_for_send[IND], reply_markup=keyboard)
@dp.callback_query_handler(text="next_vision_films")
async def next_vision_films_v1(call: types.CallbackQuery):
    global last_send_message, IND, text_for_send
    IND += 1
    keyboard = [[InlineKeyboardButton(text="◀️ Предыдущий", callback_data="back_vision_films"),
                 InlineKeyboardButton(text="▶️ Следующий", callback_data="next_vision_films")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="vision_films")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text=text_for_send[IND], reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text(text=text_for_send[IND], reply_markup=keyboard)
@dp.callback_query_handler(text="back_vision_films")
async def back_vision_films_v1(call: types.CallbackQuery):
    global last_send_message, IND, text_for_send
    IND -= 1
    keyboard = [[InlineKeyboardButton(text="◀️ Предыдущий", callback_data="back_vision_films"),
                 InlineKeyboardButton(text="▶️ Следующий", callback_data="next_vision_films")],
                [InlineKeyboardButton(text="❌ Назад", callback_data="vision_films")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(text=text_for_send[IND], reply_markup=keyboard)
    else:
        last_send_message = await call.message.edit_text(text=text_for_send[IND], reply_markup=keyboard)





















#Обработка Callback-вызовов в меню помощи
@dp.callback_query_handler(text="main_menu", state=SearchState.MODE)
async def main_menu(call: types.CallbackQuery, state=SearchState.MODE):
    global last_send_message
    await state.finish()
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(tx.KB_MAIN_TEXT.header.format(name=call.message.from_user.full_name),
                              reply_markup=kb.menu_kb1)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_MAIN_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb1)
@dp.callback_query_handler(text="main_menu2")
async def main_menu2(call: types.CallbackQuery):
    global last_send_message
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(tx.KB_MAIN_TEXT.header.format(name=call.message.from_user.full_name),
                              reply_markup=kb.menu_kb1)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_MAIN_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb1)
@dp.callback_query_handler(text="main_menu3", state=BuyFilm.MODE)
async def main_menu(call: types.CallbackQuery, state=BuyFilm.MODE):
    global last_send_message
    await state.finish()
    if call.message.photo:
        await last_send_message.delete()
        last_send_message = await call.message.answer(tx.KB_MAIN_TEXT.header.format(name=call.message.from_user.full_name),
                              reply_markup=kb.menu_kb1)
    else:
        last_send_message = await call.message.edit_text(
            tx.KB_MAIN_TEXT.header.format(name=call.message.from_user.full_name),
            reply_markup=kb.menu_kb1)
@dp.callback_query_handler(text="message_help")
async def message_help(call: types.CallbackQuery):
    await call.message.edit_text(tx.KB_HELP_TEXT.header.format(name=call.message.from_user.full_name),
                              reply_markup=kb.menu_kb2)
@dp.callback_query_handler(text="help_random")
async def help_random(call: types.CallbackQuery):
    await call.message.edit_text(tx.HELP_TEXT.RANDOM.format(name=call.message.from_user.full_name),
                              reply_markup=kb.kb_help_text)
@dp.callback_query_handler(text="help_generation")
async def help_generation(call: types.CallbackQuery):
    await call.message.edit_text(tx.HELP_TEXT.GENERATION.format(name=call.message.from_user.full_name),
                              reply_markup=kb.kb_help_text)
@dp.callback_query_handler(text="help_vision")
async def help_vision(call: types.CallbackQuery):
    await call.message.edit_text(tx.HELP_TEXT.VISION.format(name=call.message.from_user.full_name),
                              reply_markup=kb.kb_help_text)
@dp.callback_query_handler(text="help_search")
async def help_search(call: types.CallbackQuery):
    await call.message.edit_text(tx.HELP_TEXT.SEARCH.format(name=call.message.from_user.full_name),
                              reply_markup=kb.kb_help_text)
@dp.callback_query_handler(text="help_buy")
async def help_buy(call: types.CallbackQuery):
    await call.message.edit_text(tx.HELP_TEXT.BUY.format(name=call.message.from_user.full_name),
                              reply_markup=kb.kb_help_text)



def rename1():
    schedule.every().day.at('00:40').do(rename2)
    while True:
        schedule.run_pending()

def rename2():
    global no_update_urls, output
    db_path = './database/database.db'
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    updated_urls = update_zetflix_urls(db, cur)
    i = 0
    for updated_url in updated_urls:
        cur.execute("UPDATE urlbase SET film_zetflix = ? WHERE film_zetflix = ?", (updated_url, no_update_urls[i]))
        i += 1
    print(f"Ссылок обновлено - {len(output)}")
    db.commit()
    db.close()

def update_zetflix_urls(connection, cursor):
    global no_update_urls,output
    current_date = datetime.datetime.now().strftime('%d%b').lower()
    results = cursor.execute("""SELECT film_zetflix FROM urlbase""")
    no_update_urls = []
    updated_urls = []
    output = []
    for item in results:
        zetflix_url = item[0]
        no_update_urls.append(zetflix_url)
        end = zetflix_url.find('.')
        if len(zetflix_url) > 4:
            updated_url = zetflix_url[0:8] + str(current_date) + zetflix_url[end:]
            output.append(updated_url)
        else:
            updated_url = zetflix_url
        updated_urls.append(updated_url)
    return updated_urls

async def polling():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling()

def background_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

async def main():
    global history
    history = []
    loop = asyncio.get_event_loop()
    tasks = [polling()]
    await asyncio.gather(*tasks)

def start():
    rename2()
    background_thread(rename1)  # Запуск rename1 в отдельном потоке
    asyncio.run(main())

if __name__ == '__main__':
    start()