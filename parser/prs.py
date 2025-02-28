from bs4 import BeautifulSoup
import time, datetime, sqlite3, subprocess
import requests, re, json


class get():
    def wikipedia(url):
        global result, lenght
        text1 = None
        text2 = None
        if url == 'None':
            result.append('None')
            result.append(lenght)
            return
        else:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Извлекаем Количество сезонов и серий
                    table = soup.find('table')
                    if table:
                        tbody = table.find('tbody')
                        if tbody:
                            trs = tbody.find_all('tr')
                            for tr in trs:
                                th = tr.find('th', {'class': 'plainlist'})
                                if th:
                                    if th.text.strip() == 'Сезонов':
                                        td = tr.find('td', {'class': 'plainlist'})
                                        if td:
                                            text1 = td.text.strip()
                                    elif th.text.strip() == 'Серий':
                                        td = tr.find('td', {'class': 'plainlist'})
                                        if td:
                                            text2 = td.text.strip()
                                            text2 = re.sub(r'\([^)]*\)', '', text2).strip()
                                    else:
                                        continue
                                else:
                                    continue
                            result.append('None') if text1 == None else result.append(text1)
                            result.append(lenght) if text2 is None else result.append(text2)
                        else:
                            print('Error tbody')
                            return False
                    else:
                        print('Error table')
                        return False

                    return True

                else:
                    print(f"HTTP Error {response.status_code}")

            except Exception as e:
                result.append('None')
                result.append(lenght)
                print("Произошла ошибка: ", e)
    def kinopoisk(movie_id):
        api_key = "4a7ba7f7-31b6-4df3-8308-827ce7c1deb0"
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{movie_id}"
        command = [
            "curl",
            "-X", "GET",
            url,
            "-H", "accept: application/json",
            "-H", f"X-API-KEY: {api_key}"
        ]

        try:
            result = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )
            stdout, stderr = result.communicate()

            if result.returncode == 0:
                return stdout
            else:
                print(f"Ошибка при выполнении команды: {stderr}")
                return None
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e.stderr}")
            return None

def generate_id():
    global result
    bd = sqlite3.connect('database\\database.db')
    cur = bd.cursor()

    spisok = []
    results = cur.execute("""SELECT film_id FROM database """).fetchall()
    if not results:
        index = 0
    else:
        for item in results:
            spisok.append(item[0])
        max_index = max(spisok)
        index = max_index + 1
    print('ID - ' + str(index))
    result.append(index)
def save_data_to_file(data):
    global result, lenght
    dictionary = ['nameRu', 'posterUrl', 'ratingKinopoisk', 'year', 'description']
    for key, value in data.items():
        if key in dictionary:
            result.append(value)
        elif key == 'genres':
            for genre in value:
                result.append(genre['genre'])
                break
        elif key == 'countries':
            for countries in value:
                result.append(countries['country'])
                break
        elif key == 'filmLength':
            lenght = value
        else:
            continue


def main(url_kino, url_wiki, serial, lord, zet, tvigle, hd, mult):
    global result, start
    start = time.time()
    result = []
    # Генерация ID
    generate_id()
    # Парсинг Кинопоиска
    id = url_kino.split('/')[-1]
    if len(id) > 0:
        pass
    else:
        id = url_kino.split('/')[-2]
    json_data = get.kinopoisk(id)
    if json_data:
        data_dict = json.loads(json_data)  # Преобразование строки JSON в словарь
        save_data_to_file(data_dict)
    # Парсинг Википедиа
    get.wikipedia(url_wiki)
    # Добавление других платформ
    result.append(url_kino)
    result.append(serial)
    result.append(lord)
    result.append(url_wiki)

    if zet != 'None':
        current_date = datetime.datetime.now().strftime('%d%b').lower()
        index = zet.find('.')
        zet = zet[0:8:1] + str(current_date) + zet[index::1]
        print(zet)

    result.append(zet)
    result.append(tvigle)
    result.append(hd)
    result.append(mult)

    end = str(time.time() - start)
    print(f"Время парсинга - {end[2:5:1]}мс")
    if len(result) == 18:
        return result
    else:
        return False

if __name__ == "__main__":
    url = 'https://www.kinopoisk.ru/series/1274280'
    url2 = 'None'
    #url2 = 'https://ru.wikipedia.org/wiki/%D0%92%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D0%BB%D0%B8%D0%BD_%D0%BA%D0%BE%D0%BB%D0%B5%D1%86:_%D0%92%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%89%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BA%D0%BE%D1%80%D0%BE%D0%BB%D1%8F'
    print(main(url, url2, None, None, 'https://11aug.zetfix.online/serials/vinland-saga/', None, None, None))
