import schedule
import sqlite3
from googletrans import Translator
import requests
import aiohttp
import asyncio


async def delete_message(self, ch_id, msg_id):
    await self.delete_message(chat_id=ch_id, message_id=msg_id)

def create_database(name):
    import sqlite3

    path = './users/' + str(name) + '.db'
    open(path, 'w').close()
    db = sqlite3.connect(path)
    cur = db.cursor()

    cur.execute("""CREATE TABLE favorit (
    data text, 
    film_id integer,
    film_name text)""")
    db.commit()
    cur.execute("""CREATE TABLE viewed (
        data text,
        film_id integer,
        film_name text)""")
    cur.execute("""CREATE TABLE history (
            film_id integer,
            film_name text)""")
    cur.execute("""CREATE TABLE last_films (
                film_id integer,
                film_name text)""")
    cur.execute("""CREATE TABLE last_message (
                    chat_id text,
                    message_id text,
                    text text)""")
    db.commit()
    db.close()
    print('Create DataBase for User - ' + str(name))

def search_film_genre(genre='None'):
    import sqlite3
    db = sqlite3.connect('./database/database.db')
    cur = db.cursor()

    text_for_execute = 'SELECT film_id FROM database WHERE film_genre = ?'
    list_films1 = cur.execute(text_for_execute, (genre,)).fetchall()

    list_films2 = [film[0] for film in list_films1]
    return list_films2

def search_film_country(country='None'):
    import sqlite3
    db = sqlite3.connect('./database/database.db')
    cur = db.cursor()

    text_for_execute = 'SELECT film_id FROM filminfo WHERE film_country = ?'
    list_films1 = cur.execute(text_for_execute, (country,)).fetchall()

    list_films2 = [film[0] for film in list_films1]
    return list_films2



def select_film_info(id):
    import sqlite3

    text_for_execute1 = """SELECT * FROM database WHERE film_id = ?"""
    text_for_execute2 = """SELECT film_img, film_description, film_rating, film_country FROM filminfo WHERE film_id = ?"""
    text_for_execute3 = """SELECT film_kinopoisk, film_serialfan, film_lordfilms, film_wiki, film_zetflix, film_tvigle,
     film_hd, film_mult FROM urlbase WHERE film_id = ?"""

    db = sqlite3.connect('./database/database.db')
    cur = db.cursor()

    film_parametr  = list(cur.execute(text_for_execute1, (id,)).fetchone())
    film_parametr2 = list(cur.execute(text_for_execute2, (id,)).fetchone())
    film_parametr3 = list(cur.execute(text_for_execute3, (id,)).fetchone())
    film_parametr += film_parametr2 + film_parametr3
    return film_parametr

def text_to_send():
    db = sqlite3.connect('./database/database.db')
    cur = db.cursor()
    results = cur.execute("SELECT film_id, film_description FROM filminfo").fetchall()
    for id, description in results:
        if len(description) >= 1000:
            description2 = description.replace(" ", " ")
            print(f"ID: {id}, Длина_до: {len(description)}, Длина_после: {len(description2)}")




def work():
    url = 'http://www.boredapi.com/api/activity?participants=1'
    response = requests.get(url)
    translator = Translator()
    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        translated = translator.translate(activity, src='en', dest='ru')
        return translated.text
    else:
        return None
async def cat2():
    url = 'https://meowfacts.herokuapp.com/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Проверка на успешный ответ сервера
                data = await response.json()
                entry = data.get("data")[0]

                translator = Translator()
                translated = translator.translate(entry, src='en', dest='ru')

                return translated.text
    except aiohttp.ClientError as e:
        print("Ошибка при выполнении запроса:", e)
        return None

async def cat3():
    url = 'https://cataas.com/cat'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Проверка на успешный ответ сервера

                content_disposition = response.headers.get('content-disposition')
                filename = content_disposition.split('filename=')[-1].strip('"') if content_disposition else 'cat_image.jpg'

                with open(filename, 'wb') as file:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        file.write(chunk)
    except aiohttp.ClientError as e:
        return False


def jok():
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)
    translator = Translator()
    if response.status_code == 200:
        data = response.json()
        jok = data.get("setup")
        punch = data.get("punchline")
        jok = translator.translate(jok, src='en', dest='ru')
        punch = translator.translate(punch, src='en', dest='ru')
        text = f"{jok.text}\n{punch.text}"
        return text
    else:
        return None

def duck():
    url = 'https://random-d.uk/api/v1/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image = data.get("url")
        return image
    else:
        return None

def api():
    url = 'https://api.publicapis.org/entries'
    response = requests.get(url)
    translator = Translator()
    if response.status_code == 200:
        data = response.json()
        data2 = data.get("entries")
        for entry in data2:
            description = entry.get("Description")
            description = translator.translate(description, src='en', dest='ru')
            print(f'{str(entry.get("API"))}: {description.text}')
        print(f"\n\nВсего API - {len(data2)}")
        #with open('api.json', 'w') as json_file:
        #    json.dump(data, json_file, indent=4)


    else:
        print("Ошибка при выполнении запроса:", response.status_code)

def test():
    print('OK')
def start():
    schedule.every(2).seconds.do(test)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    #test()
    #text_to_send()
    #cat3()
    #duck()
    #api()
    #test()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cat3())
    #cat3()

