import sqlite3, datetime

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
        index = zetflix_url.find('.')
        if len(zetflix_url) > 4:
            updated_url = zetflix_url[0:8] + str(current_date) + zetflix_url[index:]
            output.append(updated_url)
        else:
            updated_url = zetflix_url
        updated_urls.append(updated_url)

    return updated_urls
def main():
    global no_update_urls, output

    db_path = 'database\\database.db'
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

if __name__ == '__main__':
    main()
