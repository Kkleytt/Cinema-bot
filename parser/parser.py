from bs4 import BeautifulSoup
import os, glob, sqlite3


def collect(selection, existing_links):
    directory = str(os.getcwd()) + '\\data\\list\\' + str(selection) + '\\'
    html_files = glob.glob(os.path.join(directory, '*.html'))
    num_html_files = len(html_files) + 1
    j = 1
    for i in range(1, num_html_files):
        with open(f'{directory}url{i}.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        a = soup.find('main')
        film_divs = a.find_all('div', {'class': 'styles_root__ti07r'})

        for film_div in film_divs:
            a2 = film_div.find('a', {'class': 'styles_poster__gJgwz styles_root__wgbNq'})
            if a2 and 'href' in a2.attrs:
                film_link = a2['href']
                if film_link not in existing_links:
                    result2.append(film_link)
                    j += 1

def remove_duplicates(input_list):
    unique_elements = list(set(input_list))
    return unique_elements

def main():
    global result2

    '''for i in range(1, 21):
        webbrowser.open(f'https://www.kinopoisk.ru/lists/movies/popular-series/?page={i}')'''

    result2 = []
    selection = [name for name in os.listdir('data\\list') if os.path.isdir(os.path.join('data\\list', name))]

    db = sqlite3.connect('database\\database.db')
    cur = db.cursor()

    result = list(cur.execute("""SELECT film_kinopoisk FROM urlbase""").fetchall())
    existing_links = {item[0] for item in result}  # Создаем множество существующих ссылок

    for item in selection:
        collect(item, existing_links)

    result = remove_duplicates(result2)

    f = open('kino.txt', 'w', encoding='utf-8')
    for link in result:
        f.write(f'{link}\n')

    print(f"\nФильмов записано - {len(result)}")

if __name__ == '__main__':
    main()
