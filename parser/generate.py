import customtkinter as CTk
import subprocess, os, webbrowser
import json, pyperclip
import win32api, keyboard, time, datetime
import shutil, glob


class App(CTk.CTk):
    # noinspection PyTypeChecker
    def __init__(self):
        super().__init__()
        global url_kino
        url_kino = 'None'


        # Обработка нажатий клавиатуры
        keyboard.add_hotkey('Ctrl + 1', lambda: webbrowser.open('https://www.kinopoisk.ru/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 2', lambda: webbrowser.open('https://ru.wikipedia.org/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 3', lambda: webbrowser.open('https://myseria.vip/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 4', lambda: webbrowser.open('https://ve.lordfilm.film/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 5', lambda: webbrowser.open('https://14aug.zetfix.online/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 6', lambda: webbrowser.open('https://www.tvigle.ru/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 7', lambda: webbrowser.open('https://hd.kinopoisk.ru/', new=0, autoraise=True))
        keyboard.add_hotkey('Ctrl + 8', lambda: webbrowser.open('https://multfilms.online/', new=0, autoraise=True))

        # Главное окно Приложения
        self.geometry("580x450")
        self.title("Add Data In Database")
        self.resizable(False, False)
        CTk.set_appearance_mode('dark')

        # Поля ввода
        self.entry1 = CTk.CTkTextbox(master=self, width=580, height=375, wrap='none', state='normal',
                                     font=("Arial, Helvetica, sans-serif", 20))

        # Кнопки
        self.but1 = CTk.CTkButton(master=self, text="Save", command=self.on_button1_click, width=180, height=60,
                                  font=("Arial, Helvetica, sans-serif", 21))
        self.but2 = CTk.CTkButton(master=self, text="App", command=self.on_button2_click, width=180, height=60,
                                  font=("Arial, Helvetica, sans-serif", 21))
        self.but3 = CTk.CTkButton(master=self, text="Data", command=self.on_button3_click, width=180, height=60,
                                  font=("Arial, Helvetica, sans-serif", 21))


        # Размещение
        self.entry1.place(relx=0, rely=0)

        self.but1.place(relx=0, rely=0.866666)
        self.but2.place(relx=0.344827, rely=0.866666)
        self.but3.place(relx=0.689655, rely=0.866666)



    def on_button1_click(self):
        global url_kino, name
        if os.path.exists('data\\url.txt') == False:
            with open('data\\url.txt', 'w'):
                pass
        tx1 = self.entry1.get("0.0", "end")
        tx1 = tx1.split('\n')

        if len(tx1) != 10 or tx1[0][0:6:1] == 'Ошибка':
            self.reading()

        tx = self.entry1.get("0.0", "end")
        tx2 = str(text_reading) + '\n'
        tx1 = tx.split('\n')

        if len(tx1) == 10 and tx != tx2:
            self.copy()
            name = str(tx1[0])[6::1]
            url_kino = str(tx1[1][11::1])
            url_wiki = str(tx1[2])[11::1]
            url_serialfan = str(tx1[3])[11::1]
            url_lord = str(tx1[4])[10::1]
            url_zet = str(tx1[5])[9::1]
            url_tvigle = str(tx1[6])[8::1]
            url_hd = str(tx1[7])[13::1]
            url_mult = str(tx1[8])[12::1]

            url_wiki = 'None' if len(url_wiki) < 10 else url_wiki
            url_serialfan = 'None' if len(url_serialfan) < 10 else url_serialfan
            url_lord = 'None' if len(url_lord) < 10 else url_lord
            url_zet = 'None' if len(url_zet) < 10 else url_zet
            url_tvigle = 'None' if len(url_tvigle) < 10 else url_tvigle
            url_hd = 'None' if len(url_hd) < 10 else url_hd
            url_mult = 'None' if len(url_mult) < 10 else url_mult

            text = f"{name}:\n{url_kino}\n{url_wiki}\n{url_serialfan}\n{url_lord}\n{url_zet}\n{url_tvigle}\n{url_hd}\n{url_mult}\n"
            with open('data\\url.txt', 'a', encoding='utf-8') as f:
                f.write(text)

            print(f'Фильм {name} успешно записан в файл')

            with open('data\\kino.txt', 'r', encoding='utf-8') as f:
                text = f.readlines()
            f = open('data\\kino.txt', 'w', encoding='utf-8')
            for i in range(0, len(text)):
                if text[i].replace('\n', '') == url_kino:
                    continue
                else:
                    f.write(text[i])
            f.close()
            self.reading()

        else:
            print('Ошибка в данных')
            return False



    def on_button2_click(self):
        try:
            program_file_path = os.path.abspath('app.py')
            if os.path.exists(program_file_path):
                subprocess.Popen(['python', program_file_path])
                return True
            else:
                print(f"Program file '{program_file_path}' not found.")
                return False
        except Exception as e:
            print("Error occurred:", e)
            return False
    def on_button3_click(self):
        db_file_path = os.getcwd() + '\\database\\database.db'
        program_name = os.getcwd() + '\\DB browser\\app.exe'
        try:
            root_dir = os.path.dirname(os.path.abspath(db_file_path))
            program_path = os.path.join(root_dir, program_name)
            if not os.path.exists(program_path):
                print(f"Program '{program_name}' not found in the directory.")
                return False
            subprocess.Popen(f'"{program_path}" "{db_file_path}"', shell=True)
            return True
        except Exception as e:
            print("Error occurred:", e)
            return False
    def reading(self):
        global url_kino, text_reading
        if os.path.exists('data\\kino.txt') == False:
            self.entry1.delete("0.0", "end")
            self.entry1.insert("0.0", "Error File kino.txt")
            return
        with open('data\\kino.txt', 'r', encoding='utf-8') as f:
            url_kino = f.readline().replace('\n', '')


        if url_kino[0:30:1] == 'https://www.kinopoisk.ru/film/':
            url = url_kino.replace('https://www.kinopoisk.ru/film/', '')
        elif url_kino[0:32:1] == 'https://www.kinopoisk.ru/series/':
            url = url_kino.replace('https://www.kinopoisk.ru/series/', '')
        url = url[0:-1:1]
        read = self.kinopoisk(url)
        print(read[0])
        if read[0] == None:
            print('OK')
            with open('data\\kino.txt', 'r', encoding='utf-8') as f:
                text = f.readlines()
            f = open('data\\kino.txt', 'w', encoding='utf-8')
            for i in range(0, len(text)):
                if text[i].replace('\n', '') == url_kino:
                    continue
                else:
                    f.write(text[i])
            with open('data\\kino.txt', 'r', encoding='utf-8') as f:
                url = f.readline().replace('\n', '')
            read = self.kinopoisk(url)
        self.write(read[0])
        if len(read) == 2:
            text_reading = f"Name: {read[0]} ({read[1]})\nKinopoisk: {url_kino}\nWikipedia: \nSerialFan: \nLordFilm: \nZetFlix: \nTvigle: \n" \
                   f"KinopoiskHD: \nMultOnline: "
        elif read == None:
            text_reading = f"Ошибка в ссылке {url_kino}"
        self.entry1.delete("0.0", "end")
        self.entry1.insert("0.0", text_reading)


    def kinopoisk(self, url):
        api_key = "4a7ba7f7-31b6-4df3-8308-827ce7c1deb0"
        url_kino = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{url}"
        text = []

        command = [
            "curl",
            "-X", "GET",
            url_kino,
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
                data = json.loads(stdout)
                for key, value in data.items():
                    if key == 'nameRu' or key == 'year':
                        text.append(value)
                    else:
                        continue
                return text
            else:
                print(f"Ошибка при выполнении команды: {stderr}")
                return None
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e.stderr}")
            return None

    # Копирует в буфер обмена информацию
    def write(self, name):
        a = win32api.GetKeyboardLayout()
        if a == 68748313:
            win32api.LoadKeyboardLayout('00000409', 1)
        elif a == 67699721:
            pass
        pyperclip.copy(name)

    def copy(self):
        backup_time = datetime.datetime.now().strftime('%d.%m-%H.%M.%S')
        backup_dir = "backup\\" + backup_time
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        if not os.path.exists(backup_dir + '\\App'):
            os.makedirs(backup_dir + '\\App')

        print('Backup Create')

        files_to_backup = ['data\\kino.txt', 'data\\url.txt', 'database\\database.db', 'input.txt', 'history\\history.txt']
        for file_path in files_to_backup:
            file_name = os.path.basename(file_path)
            backup_file_path = os.path.join(backup_dir, f"{file_name}")
            try:
                shutil.copyfile(file_path, backup_file_path)
            except Exception as e:
                print(f"Error creating backup for {file_name}: {e}")

        code_to_backup = ['app.py', 'generate.py', 'parser.py', 'prs.py', 'test.py', 'tst.py']
        for code in code_to_backup:
            file_name = os.path.basename(code)
            backup_file_path = os.path.join(backup_dir + '\\App', f"{file_name}")
            try:
                shutil.copyfile(code, backup_file_path)
            except Exception as e:
                print(f"Error creating backup for {file_name}: {e}")

        # Удаление старых бекапов, оставляя не более трех
        existing_backups = glob.glob("backup\\*")
        existing_backups.sort(reverse=True)
        backups_to_keep = existing_backups[:5]

        for backup in existing_backups:
            if backup not in backups_to_keep:
                try:
                    shutil.rmtree(backup)
                    print(f"Delete old backup: {backup}")
                except Exception as e:
                    print(f"Error deleting backup: {backup}: {e}")




if __name__ == "__main__":
    start = time.time()
    try:
        app = App()
        app.mainloop()
    except Exception as ex:
        print(f'Error - {ex}')
    finally:
        end = str(time.time() - start)
        index = end.find('.')
        end = int(end[0:index])

        if end > 60 and end < 3600:
            print(f"Время работы программы - {end // 60}:{end - ((end // 60) * 60)} мин")
        elif end > 3600:
            print(f"Время работы программы - {end // 3600}:{end - ((end // 3600) * 3600)} ч")
        else:
            print(f"Время работы программы - {end}с")
