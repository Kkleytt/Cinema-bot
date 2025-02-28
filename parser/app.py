import subprocess, webbrowser, os
import customtkinter as CTk
import prs, pyperclip, keyboard
import shutil, sqlite3


class ToplevelWindow(CTk.CTkToplevel):
    def __init__(self):
        super().__init__()
        color1 = '#45A054'
        color2 = '#0B5F18'
        self.geometry("300x500")
        CTk.set_appearance_mode('dark')

        self.txbox = CTk.CTkTextbox(self, width=300, height=440)
        self.bt1 = CTk.CTkButton(master=self, width=300, height=50, font=("Arial, Helvetica, sans-serif", 16),
                                 text='Delete Index', fg_color=color1, hover_color=color2,
                                 command=self.delete)
        self.txbox.place(relx=0, rely=0)
        self.bt1.place(relx=0, rely=0.9)

    def delete(self):
        text = self.txbox.get('0.0', 'end').split('\n')
        indexs = []
        for item in text:
            if item == '':
                continue
            else:
                indexs.append(item)

        conn = sqlite3.connect("database\\database.db")
        cursor = conn.cursor()
        self.txbox.delete('0.0', 'end')
        for index in indexs:
            try:
                # Удаляем только одну строку с заданным индексом
                all = list(cursor.execute("SELECT rowid FROM database WHERE film_id = ?", (index,)).fetchall())
                cursor.execute("DELETE FROM database WHERE rowid = ?", (all[1][0],))
                cursor.execute("DELETE FROM filminfo WHERE rowid = ?", (all[1][0],))
                cursor.execute("DELETE FROM urlbase WHERE rowid = ?", (all[1][0],))
                conn.commit()
                print(f"Первая строка под индексом {all[1][0]} успешно удалена")
            except sqlite3.Error as e:
                print("Произошла ошибка:", e)

        conn.close()


class App(CTk.CTk):
    def __init__(self):
        super().__init__()
        global color1, color2, auto
        color1 = '#45A054'
        color2 = '#0B5F18'
        auto = 0
        self.toplevel_window = None

        # Главное окно Приложения
        self.geometry("1000x500")
        self.title("Add Data In Database")
        self.resizable(False, False)
        CTk.set_appearance_mode('dark')

        # Обработка нажатий клавиатуры
        keyboard.add_hotkey('Ctrl + Q', self.copy)
        keyboard.add_hotkey('Ctrl + W + E', self.prinud_copy)
        keyboard.add_hotkey('Ctrl + P', self.on_button5_click)
        keyboard.add_hotkey('Ctrl + S', self.on_button6_click)
        keyboard.add_hotkey('Ctrl + F', self.on_button7_click)
        keyboard.add_hotkey('Ctrl + D', self.delete)

        # Поля ввода
        self.entry1 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='Kinopoisk')
        self.entry2 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='Wikipedia')
        self.entry3 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='SerialFan')
        self.entry4 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='LordFilm')

        self.entry5 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='Zetflix')
        self.entry6 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='Tvigle')
        self.entry7 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='KinopoiskHD')
        self.entry8 = CTk.CTkEntry(master=self, width=400, height=40, placeholder_text='MultFilm')

        self.slider2 = CTk.CTkLabel(master=self, width=250, height=40, fg_color='#1E1E1E', text='', corner_radius=6)
        self.slider = CTk.CTkSlider(master=self, width=200, height=20, from_=4, to=8, number_of_steps=2,
                                    border_color='#1E1E1E',corner_radius=0, border_width=6, progress_color=color1,
                                    button_color=color2, hover=False, command=self.slider_def)
        self.slider.set(8)
        self.slider1 = CTk.CTkLabel(master=self, width=50, height=40, text='8', fg_color=color1,
                                    font=("Arial, Helvetica, sans-serif", 26), corner_radius=6)


        # Текстовое поле
        self.text_area = CTk.CTkTextbox(master=self, width=500, height=500, state='normal',
                                        font=("Arial, Helvetica, sans-serif", 20), wrap='none')
        self.text_area2 = CTk.CTkTextbox(master=self, width=500, height=500, state='normal',
                                        font=("Arial, Helvetica, sans-serif", 14), wrap='none')
        self.text_area3 = CTk.CTkTextbox(master=self, width=500, height=500, state='normal',
                                         font=("Arial, Helvetica, sans-serif", 14), wrap='none')
        self.text_area4 = CTk.CTkTextbox(master=self, width=290, height=240, state='disabled',
                                         font=("Arial, Helvetica, sans-serif", 14), wrap='word')
        self.text_area5 = CTk.CTkTextbox(master=self, width=130, height=340, state='disabled',
                                         font=("Arial, Helvetica, sans-serif", 14), wrap='word')

        # Кнопки
        self.label1 = CTk.CTkTextbox(master=self, width=400, height=40, wrap='none',
                                     font=("Arial, Helvetica, sans-serif", 23))
        self.label1.insert("0.0", '                         Settings')
        self.label1.configure(state='disabled')

        self.button1 = CTk.CTkButton(master=self, text="", command=self.on_button1_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button2 = CTk.CTkButton(master=self, text="", command=self.on_button2_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button3 = CTk.CTkButton(master=self, text="", command=self.on_button3_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button4 = CTk.CTkButton(master=self, text="", command=self.on_button4_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button21 = CTk.CTkButton(master=self, text="", command=self.on_button21_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button22 = CTk.CTkButton(master=self, text="", command=self.on_button22_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button23 = CTk.CTkButton(master=self, text="", command=self.on_button23_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)
        self.button24 = CTk.CTkButton(master=self, text="", command=self.on_button24_click, width=40, height=40,
                                     fg_color=color1, hover_color=color2)

        self.button5 = CTk.CTkButton(master=self, text="Parcing", command=self.on_button5_click, width=130, height=50,
                                     fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 16))
        self.button6 = CTk.CTkButton(master=self, text="Save", command=self.on_button6_click, width=130, height=50,
                                     fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 16))
        self.button7 = CTk.CTkButton(master=self, text="File", command=self.on_button7_click, width=130, height=50,
                                     fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 16))

        self.button8 = CTk.CTkButton(master=self, text="🡆", command=self.on_button8_click, width=85, height=40,
                                     fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 30))
        self.button9 = CTk.CTkButton(master=self, text="🡆", command=self.on_button9_click, width=85, height=40,
                                     fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 30))
        self.button10 = CTk.CTkButton(master=self, text="🡆", command=self.on_button10_click, width=85, height=40,
                                     fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 30))
        self.button11 = CTk.CTkButton(master=self, text="🡆", command=self.on_button11_click, width=85, height=40,
                                      fg_color=color1, hover_color=color2, font=("Arial, Helvetica, sans-serif", 30))

        self.button12 = CTk.CTkButton(master=self, text="Set Date", command=self.on_button12_click, width=130, height=50,
                                      fg_color='#1E1E1E', hover_color=color2, font=("Arial, Helvetica, sans-serif", 18))
        self.button13 = CTk.CTkButton(master=self, text="Auto", command=self.on_button13_click, width=130, height=50,
                                      fg_color="#1E1E1E", hover_color=color2, font=("Arial, Helvetica, sans-serif", 18))
        self.button14 = CTk.CTkButton(master=self, text="DataBase", command=self.on_button14_click, width=130,
                                      height=40, fg_color='#1E1E1E', hover_color=color2,
                                      font=("Arial, Helvetica, sans-serif", 18))
        self.button15 = CTk.CTkButton(master=self, text="Collect app", command=self.on_button15_click, width=130,
                                      height=50, fg_color='#1E1E1E', hover_color=color2,
                                      font=("Arial, Helvetica, sans-serif", 18))
        self.button16 = CTk.CTkButton(master=self, text="Delete dubl", command=self.on_button16_click, width=130,
                                      height=40, fg_color='#1E1E1E', hover_color=color2,
                                      font=("Arial, Helvetica, sans-serif", 18))



        # Упаковка виджетов
        self.entry1.place(relx=0.025, rely=0.04)
        self.entry2.place(relx=0.025, rely=0.14)
        self.entry3.place(relx=0.025, rely=0.24)
        self.entry4.place(relx=0.025, rely=0.34)
        self.entry5.place(relx=0.025, rely=0.44)
        self.entry6.place(relx=0.025, rely=0.54)
        self.entry7.place(relx=0.025, rely=0.64)
        self.entry8.place(relx=0.025, rely=0.74)

        self.button1.place(relx=0.435, rely=0.04)
        self.button2.place(relx=0.435, rely=0.14)
        self.button3.place(relx=0.435, rely=0.24)
        self.button4.place(relx=0.435, rely=0.34)
        self.button21.place(relx=0.435, rely=0.44)
        self.button22.place(relx=0.435, rely=0.54)
        self.button23.place(relx=0.435, rely=0.64)
        self.button24.place(relx=0.435, rely=0.74)


        self.button5.place(relx=0.025, rely=0.86)
        self.button6.place(relx=0.185, rely=0.86)
        self.button7.place(relx=0.345, rely=0.86)
        self.button8.place(relx=0.92, rely=0.04)
        self.button9.place(relx=1, rely=1)
        self.button10.place(relx=1, rely=1)
        self.button11.place(relx=1, rely=1)
        self.button12.place(relx=1, rely=1)
        self.button13.place(relx=1, rely=1)
        self.button14.place(relx=1, rely=1)
        self.button15.place(relx=1, rely=1)
        self.button16.place(relx=1, rely=1)
        self.text_area.place(relx=0.5, rely=0)
        self.text_area2.place(relx=1, rely=1)
        self.text_area3.place(relx=1, rely=1)
        self.text_area4.place(relx=1, rely=1)
        self.text_area5.place(relx=1, rely=1)
        self.label1.place(relx=1, rely=1)

        text_to_write = f"ID: [0]\nName: [1]\nGenre: [2]\nYear: [3]\nSeason: [4]\nSeria: [5]\nImg: [6]\n" \
                        f"Kinopoisk: [7]\nSerialFan: [8]\nLordFilm: [9]\nWikipedia: [10]\nZetFlix: [11]\n" \
                        f"Tvigle: [12]\nKinopoiskHD: [13]\nMultFilm: [14]\nDescription: [15]\n" \
                        f"Rating: [16]\nCountry: [17]"
        self.text_area5.configure(state='normal')
        self.text_area5.insert("0.0", text_to_write)
        self.text_area5.configure(state='disabled')


    def on_button1_click(self):
        if self.entry1.get() != '':
            webbrowser.open(self.entry1.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://www.kinopoisk.ru/', new=0, autoraise=True)

    def on_button2_click(self):
        if self.entry2.get() != '':
            webbrowser.open(self.entry2.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0', new=0, autoraise=True)

    def on_button3_click(self):
        if self.entry3.get() != '':
            webbrowser.open(self.entry3.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://myseria.vip/', new=0, autoraise=True)

    def on_button4_click(self):
        if self.entry4.get() != '':
            webbrowser.open(self.entry4.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://ve.lordfilm.film/', new=0, autoraise=True)

    def on_button5_click(self):
        global vision
        url_kino = self.entry1.get()
        url_wiki = self.entry2.get()
        url_serial = self.entry3.get()
        url_lord = self.entry4.get()
        url_zet = self.entry5.get()
        url_tvigle = self.entry6.get()
        url_hd = self.entry7.get()
        url_mult = self.entry8.get()

        if url_serial == '':
            url_serial = 'None'
        if url_lord == '':
            url_lord = 'None'
        if url_zet == '':
            url_zet = 'None'
        if url_tvigle == '':
            url_tvigle = 'None'
        if url_hd == '':
            url_hd = 'None'
        if url_mult == '':
            url_mult = 'None'

        if self.entry1.get() != '' and self.entry2.get() != '':
            results = prs.main(url_kino, url_wiki, url_serial, url_lord, url_zet, url_tvigle, url_hd, url_mult)
            print(results)
            if results:
                dsc = results[5]
                if dsc != None:
                    a = dsc.find('\n')
                if a == '0':
                    pass
                else:
                    dsc = dsc.replace('\n', ' ')
                self.text_area.configure(state='normal', wrap='none')
                self.text_area.delete("0.0", 'end')
                self.text_area.insert("0.0", f"✨ID: {results[0]}\n✨Name: {results[1]}\n"
                                             f"✨Genre: {results[7]}\n✨Year: {results[4]}\n"
                                             f"✨Season: {results[8]}\n✨Seria: {results[9]}\n"
                                             f"✨Img: {results[2]}\n✨Kinopoisk: {results[10]}\n"
                                             f"✨SerialFan: {results[11]}\n✨LordFilm: {results[12]}\n"
                                             f"✨Wikipedia: {results[13]}\n✨ZetFlix: {results[14]}\n"
                                             f"✨Tvigle: {results[15]}\n✨KinopoiskHD: {results[16]}\n"
                                             f"✨MultFilm: {results[17]}\n✨Description: {dsc}\n"
                                             f"✨Rating: {results[3]}\n✨Country: {results[6]}")
                self.write(results[1])

    def write(self, name):
        pyperclip.copy(name)  # Копирует в буфер обмена информацию
        pyperclip.paste()

    def on_button6_click(self):
        import sqlite3
        db = sqlite3.connect("database\\database.db")
        cur = db.cursor()

        text = self.text_area.get("0.0", "end")
        text2 = text.split('\n')
        print(len(text2))
        if len(text2) != 19:
            self.button6.configure(text='Error len text', fg_color='#BD2C2C', hover_color='#7E1818')
            return
        else:
            self.button6.configure(text='Save',
                                   fg_color=color1, hover_color=color2)
        text = text.replace("\n", "").split("✨")
        text = text[1:]

        sel_list = []
        sel_list.append(text[0][4::1])
        sel_list.append(text[1][6::1])
        sel_list.append(text[2][7::1])
        sel_list.append(text[3][6::1])
        sel_list.append(text[4][8::1])
        sel_list.append(text[5][7::1])
        sel_list.append(text[6][5::1])
        sel_list.append(text[7][11::1])
        sel_list.append(text[8][11::1])
        sel_list.append(text[9][10::1])
        sel_list.append(text[10][11::1])
        sel_list.append(text[11][9::1])
        sel_list.append(text[12][8::1])
        sel_list.append(text[13][13::1])
        sel_list.append(text[14][10::1])
        sel_list.append(text[15][13::1])
        sel_list.append(text[16][8::1])
        sel_list.append(text[17][9::1])

        for item in sel_list:
            print(item)


        # Добавление в БД
        cur.execute("""INSERT INTO database VALUES (?, ?, ?, ?, ?, ?)""",
                    (sel_list[0], sel_list[1], sel_list[2], sel_list[3], sel_list[4], sel_list[5]))
        cur.execute("""INSERT INTO filminfo VALUES (?, ?, ?, ?, ?, ?)""",
                    (sel_list[0], sel_list[1], sel_list[6], sel_list[15], sel_list[16], sel_list[17]))
        cur.execute("""INSERT INTO urlbase VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (sel_list[0], sel_list[1], sel_list[7], sel_list[8], sel_list[9], sel_list[10], sel_list[11],
                     sel_list[12], sel_list[13], sel_list[14]))
        print('\nДанные записаны')
        db.commit()
        db.close()

    def on_button7_click(self):
        if os.path.exists('history') == False:
            os.mkdir('history')
        if os.path.exists('history\\history.txt') == False:
            with open('history\\history.txt', 'w'):
                pass
        read = open('input.txt', 'r', encoding='utf-8')
        write = open('history\\history.txt', 'a', encoding='utf-8')
        read.close()
        read = open('input.txt', 'r', encoding='utf-8')

        a1 = read.readline()
        a2 = read.readline()
        a2 = a2[0:-1:1]
        a3 = read.readline()
        a3 = a3[0:-1:1]
        a4 = read.readline()
        a4 = a4[0:-1:1]
        a5 = read.readline()
        a5 = a5[0:-1:1]
        a6 = read.readline()
        a6 = a6[0:-1:1]
        a7 = read.readline()
        a7 = a7[0:-1:1]
        a8 = read.readline()
        a8 = a8[0:-1:1]
        a9 = read.readline()
        a9 = a9[0:-1:1]

        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')
        self.entry3.delete(0, 'end')
        self.entry4.delete(0, 'end')
        self.entry5.delete(0, 'end')
        self.entry6.delete(0, 'end')
        self.entry7.delete(0, 'end')
        self.entry8.delete(0, 'end')

        if a2[0:24:1] == 'https://www.kinopoisk.ru' or a2[0:24:1] == 'None':
            self.entry1.insert(0, a2)
        else:
            self.entry1.insert(0, 'Ошибка Kinopoisk, проверьте правильность заполнения файла')

        if a3[0:24:1] == 'https://ru.wikipedia.org' or a3[0:24:1] == 'None':
            self.entry2.insert(0, a3)
        else:
            self.entry2.insert(0, 'Ошибка Wikipedia, проверьте правильность заполнения файла')

        if a4[0:19:1] == 'https://myseria.vip' or a4[0::1] == 'None':
            self.entry3.insert(0, a4)
        else:
            self.entry3.insert(0, 'Ошибка SerialFan, проверьте правильность заполнения файла')

        if a5[0:24:1] == 'https://h1.lordfilm.film' or a5[0:24:1] == 'https://ve.lordfilm.film' or a5[0:24:1] == 'None':
            self.entry4.insert(0, a5)
        else:
            self.entry4.insert(0, 'Ошибка LordFilm, проверьте правильность заполнения файла')

        if a6[0:28:1] == 'https://14aug.zetfix.online/' or a6[0:24:1] == 'None':
            self.entry5.insert(0, a6)
        else:
            self.entry5.insert(0, 'Ошибка ZetFlix, проверьте правильность заполнения файла')

        if a7[0:22:1] == 'https://www.tvigle.ru/' or a7[0:24:1] == 'None':
            self.entry6.insert(0, a7)
        else:
            self.entry6.insert(0, 'Ошибка Tvigle, проверьте правильность заполнения файла')

        if a8[0:24:1] == 'https://hd.kinopoisk.ru/' or a8[0:24:1] == 'None':
            self.entry7.insert(0, a8)
        else:
            self.entry7.insert(0, 'Ошибка KinopoiskHD, проверьте правильность заполнения файла')

        if a9[0:24:1] == 'https://multfilms.online' or a9[0:24:1] == 'None':
            self.entry8.insert(0, a9)
        else:
            self.entry8.insert(0, 'Ошибка MultFilm, проверьте правильность заполнения файла')



        write.write(a1)
        write.write(a2 + '\n')
        write.write(a3 + '\n')
        write.write(a4 + '\n')
        write.write(a5 + '\n')
        write.write(a6 + '\n')
        write.write(a7 + '\n')
        write.write(a8 + '\n')
        write.write(a9 + '\n')

        write.close()
        read.close()

        read = open('input.txt', 'r', encoding='utf-8')
        strings = read.readlines()
        read.close()

        cache = open('cache.txt', 'w', encoding='utf-8')
        for i in range(9, len(strings)):
            cache.write(strings[i])

        cache.close()
        os.remove('input.txt')
        os.rename('cache.txt', 'input.txt')

    def on_button8_click(self):
        self.text_area.place(relx=1, rely=1)
        self.text_area2.place(relx=0.5, rely=0)
        self.text_area3.place(relx=1, rely=1)
        self.button8.place(relx=1, rely=1)
        self.button9.place(relx=0.92, rely=0.04)
        self.button10.place(relx=1, rely=1)
        self.button11.place(relx=1, rely=1)
        self.button12.place(relx=1, rely=1)

        with open('input.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        self.text_area2.configure(state='normal')
        self.text_area2.delete('0.0', 'end')
        self.text_area2.insert('0.0', 'Входные данные:\n' + str(text))
        self.text_area2.configure(state='disabled')

    def on_button9_click(self):
        if os.path.exists('history') == False:
            os.mkdir('history')
        if os.path.exists('history\\history.txt') == False:
            with open('history\\history.txt', 'w'):
                pass
        self.text_area.place(relx=1, rely=1)
        self.text_area2.place(relx=1, rely=1)
        self.text_area3.place(relx=0.5, rely=0)
        self.button8.place(relx=1, rely=1)
        self.button9.place(relx=1, rely=1)
        self.button10.place(relx=0.92, rely=0.04)

        with open('history\\history.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        self.text_area3.configure(state='normal')
        self.text_area3.delete('0.0', 'end')
        self.text_area3.insert('0.0', 'История:\n' + str(text))
        self.text_area3.configure(state='disabled')


    def on_button10_click(self):
        import sqlite3
        bd = sqlite3.connect("database\\database.db")
        cur = bd.cursor()
        max_db = len(list(cur.execute("SELECT film_id FROM database").fetchall()))
        with open('input.txt', 'r', encoding='utf-8') as f:
            max_txt = int(len(f.readlines()) / 9)
        with open('history\\history.txt', 'r', encoding='utf-8') as f:
            max_history = int(len(f.readlines()) / 9)

        text_to_write = f"Всего фильмов в БД: {max_db}\nВсего фильмов в файле: " \
                        f"{max_txt}\n\nСочетания клавиш:\nCtrl + Q - Копирование url\n" \
                        f"Ctrl + W + E - Копирование url v2\nCtrl + D - Удаления дубликатов\nCtrl + P - Парсинг\nCtrl + S - Сохранение в бд\nCtrl + F - Чтение из файла"

        self.text_area4.configure(state='normal')
        self.text_area4.delete("0.0", "end")
        self.text_area4.insert("0.0", text_to_write)
        self.text_area4.configure(state='disabled')

        self.text_area3.place(relx=1, rely=1)
        self.button10.place(relx=1, rely=1)

        self.button11.place(relx=0.92, rely=0.04) # Кнопка следующей страницы
        self.button12.place(relx=0.685, rely=0.86) # Кнопка Cookies
        self.button13.place(relx=0.525, rely=0.86) # Кнопка Invisible
        self.button14.place(relx=0.525, rely=0.74) # Кнопка DataBase
        self.button15.place(relx=0.845, rely=0.86) # Кнопка Creator
        self.button16.place(relx=0.685, rely=0.74) # Кнопка Later
        self.label1.place(relx=0.525, rely=0.04) # Название Настройки
        self.text_area4.place(relx=0.525, rely=0.14) # Поле слева
        self.text_area5.place(relx=0.845, rely=0.14) # Поле справа
        self.slider.place(relx=0.55, rely=0.66) # Слайдер
        self.slider1.place(relx=0.765, rely=0.64) # Номер слайдера
        self.slider2.place(relx=0.525, rely=0.64) # Фон слайера
    def on_button11_click(self):
        self.text_area.place(relx=0.5, rely=0)
        self.text_area2.place(relx=1, rely=1)
        self.text_area3.place(relx=1, rely=1)
        self.button8.place(relx=0.92, rely=0.04)
        self.button9.place(relx=1, rely=1)
        self.button10.place(relx=1, rely=1)
        self.button11.place(relx=1, rely=1)
        self.button12.place(relx=1, rely=1)
        self.button13.place(relx=1, rely=1)
        self.button14.place(relx=1, rely=1)
        self.button15.place(relx=1, rely=1)
        self.button16.place(relx=1, rely=1)
        self.label1.place(relx=1, rely=1)
        self.text_area4.place(relx=1, rely=1)
        self.text_area5.place(relx=1, rely=1)
        self.slider.place(relx=1, rely=1)  # Слайдер

    def on_button12_click(self):
        import test

        test.main()

    def on_button13_click(self):
        global auto
        if auto == 1 or auto == None:
            auto = 0
            self.button13.configure(fg_color='#1E1E1E')
            self.button5.configure(command=self.on_button5_click)
        else:
            auto = 1
            self.button13.configure(fg_color='#45A054')
            self.button5.configure(command=self.on_button25_click)

    def on_button14_click(self):
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

    def on_button15_click(self):
        try:
            program_file_path = os.path.abspath('generate.py')
            if os.path.exists(program_file_path):
                subprocess.Popen(['python', program_file_path])
                return True
            else:
                print(f"Program file '{program_file_path}' not found.")
                return False
        except Exception as e:
            print("Error occurred:", e)
            return False

    def on_button16_click(self):
        import sqlite3

        db = sqlite3.connect('database\\database.db')
        cursor = db.cursor()

        cursor.execute("SELECT film_kinopoisk, COUNT(*) FROM urlbase GROUP BY film_kinopoisk HAVING COUNT(*) > 1")
        kinopoisk_duplicates = cursor.fetchall()
        duplicates_info = []
        ids_to_delete = []
        for film_kinopoisk, count in kinopoisk_duplicates:
            cursor.execute("SELECT film_id, film_name FROM urlbase WHERE film_kinopoisk = ?", (film_kinopoisk,))
            films = cursor.fetchall()
            for film_id, film_name in films:
                duplicates_info.append((film_id, film_name, film_kinopoisk))
                ids_to_delete.append(film_id)
        if len(duplicates_info) > 0:
            print('\nИнформация всех дубликатов:')
        else:
            print('\nДубликаты не найдены')
        for item in duplicates_info:
            film_id, film_name, film_kinopoisk = item
            print(f"Film ID: {film_id}, Film Name: {film_name}, Kinopoisk Link: {film_kinopoisk}")



        cursor.execute("SELECT film_kinopoisk, COUNT(*) FROM urlbase GROUP BY film_kinopoisk HAVING COUNT(*) > 1")
        kinopoisk_duplicates = cursor.fetchall()
        duplicates_info = []
        original_ids = set()
        for film_kinopoisk, count in kinopoisk_duplicates:
            cursor.execute("SELECT film_id, film_name FROM urlbase WHERE film_kinopoisk = ?", (film_kinopoisk,))
            films = cursor.fetchall()
            for film_id, film_name in films:
                if film_name not in original_ids:
                    original_ids.add(film_name)
                else:
                    duplicates_info.append((film_id, film_name, film_kinopoisk))
        db.close()
        if len(duplicates_info) > 0:
            print("\nДубликаты для удаления:")
        for item in duplicates_info:
            film_id, film_name, film_kinopoisk = item
            print(f"Film ID: {film_id}, Film Name: {film_name}, Kinopoisk Link: {film_kinopoisk}")


    def slider_def(self, value):
        value = int(value)
        if value == 4:
            self.slider1.configure(text='4')

            self.entry1.configure(height=60)
            self.entry2.configure(height=60)
            self.entry3.configure(height=60)
            self.entry4.configure(height=60)

            self.entry1.place(relx=0.025, rely=0.04)
            self.entry2.place(relx=0.025, rely=0.26)
            self.entry3.place(relx=0.025, rely=0.48)
            self.entry4.place(relx=0.025, rely=0.7)

            self.button1.place(relx=0.435, rely=0.06)
            self.button2.place(relx=0.435, rely=0.28)
            self.button3.place(relx=0.435, rely=0.50)
            self.button4.place(relx=0.435, rely=0.72)

            self.entry5.place(relx=1, rely=1)
            self.entry6.place(relx=1, rely=1)
            self.entry7.place(relx=1, rely=1)
            self.entry8.place(relx=1, rely=1)
            self.button21.place(relx=1, rely=1)
            self.button22.place(relx=1, rely=1)
            self.button23.place(relx=1, rely=1)
            self.button24.place(relx=1, rely=1)
        if value == 6:
            self.slider1.configure(text='6')

            self.entry1.configure(height=50)
            self.entry2.configure(height=50)
            self.entry3.configure(height=50)
            self.entry4.configure(height=50)
            self.entry5.configure(height=50)
            self.entry6.configure(height=50)

            self.entry1.place(relx=0.025, rely=0.04)
            self.entry2.place(relx=0.025, rely=0.176)
            self.entry3.place(relx=0.025, rely=0.312)
            self.entry4.place(relx=0.025, rely=0.448)
            self.entry5.place(relx=0.025, rely=0.584)
            self.entry6.place(relx=0.025, rely=0.72)

            self.button1.place(relx=0.435, rely=0.05)
            self.button2.place(relx=0.435, rely=0.186)
            self.button3.place(relx=0.435, rely=0.322)
            self.button4.place(relx=0.435, rely=0.458)
            self.button21.place(relx=0.435, rely=0.594)
            self.button22.place(relx=0.435, rely=0.73)

            self.button23.place(relx=1, rely=1)
            self.button24.place(relx=1, rely=1)
            self.entry7.place(relx=1, rely=1)
            self.entry8.place(relx=1, rely=1)
        if value == 8:
            self.slider1.configure(text='8')

            self.entry1.configure(height=40)
            self.entry2.configure(height=40)
            self.entry3.configure(height=40)
            self.entry4.configure(height=40)
            self.entry5.configure(height=40)
            self.entry6.configure(height=40)
            self.entry7.configure(height=40)
            self.entry8.configure(height=40)

            self.entry1.place(relx=0.025, rely=0.04)
            self.entry2.place(relx=0.025, rely=0.14)
            self.entry3.place(relx=0.025, rely=0.24)
            self.entry4.place(relx=0.025, rely=0.34)
            self.entry5.place(relx=0.025, rely=0.44)
            self.entry6.place(relx=0.025, rely=0.54)
            self.entry7.place(relx=0.025, rely=0.64)
            self.entry8.place(relx=0.025, rely=0.74)

            self.button1.place(relx=0.435, rely=0.04)
            self.button2.place(relx=0.435, rely=0.14)
            self.button3.place(relx=0.435, rely=0.24)
            self.button4.place(relx=0.435, rely=0.34)
            self.button21.place(relx=0.435, rely=0.44)
            self.button22.place(relx=0.435, rely=0.54)
            self.button23.place(relx=0.435, rely=0.64)
            self.button24.place(relx=0.435, rely=0.74)

    def on_button21_click(self):
        if self.entry5.get() != '':
            webbrowser.open(self.entry5.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://14aug.zetfix.online/', new=0, autoraise=True)
    def on_button22_click(self):
        if self.entry6.get() != '':
            webbrowser.open(self.entry6.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://www.tvigle.ru/', new=0, autoraise=True)
    def on_button23_click(self):
        if self.entry7.get() != '':
            webbrowser.open(self.entry7.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://hd.kinopoisk.ru/', new=0, autoraise=True)
    def on_button24_click(self):
        if self.entry8.get() != '':
            webbrowser.open(self.entry8.get(), new=0, autoraise=True)
        else:
            webbrowser.open('https://multfilms.online', new=0, autoraise=True)
    def on_button25_click(self):
        print('OK')
        with open('input.txt', 'r', encoding='utf-8') as f:
            max_txt = int(len(f.readlines()) / 9)
        for i in range(0, max_txt):
            # Чтение файла
            if os.path.exists('history') == False:
                os.mkdir('history')
            if os.path.exists('history\\history.txt') == False:
                with open('history\\history.txt', 'w'):
                    pass
            read = open('input.txt', 'r', encoding='utf-8')
            write = open('history\\history.txt', 'a', encoding='utf-8')
            read.close()
            read = open('input.txt', 'r', encoding='utf-8')
            a1 = read.readline()
            a2 = read.readline()
            a2 = a2[0:-1:1]
            a3 = read.readline()
            a3 = a3[0:-1:1]
            a4 = read.readline()
            a4 = a4[0:-1:1]
            a5 = read.readline()
            a5 = a5[0:-1:1]
            a6 = read.readline()
            a6 = a6[0:-1:1]
            a7 = read.readline()
            a7 = a7[0:-1:1]
            a8 = read.readline()
            a8 = a8[0:-1:1]
            a9 = read.readline()
            a9 = a9[0:-1:1]
            self.entry1.delete(0, 'end')
            self.entry2.delete(0, 'end')
            self.entry3.delete(0, 'end')
            self.entry4.delete(0, 'end')
            self.entry5.delete(0, 'end')
            self.entry6.delete(0, 'end')
            self.entry7.delete(0, 'end')
            self.entry8.delete(0, 'end')
            if a2[0:24:1] == 'https://www.kinopoisk.ru' or a2[0:24:1] == 'None':
                self.entry1.insert(0, a2)
            else:
                self.entry1.insert(0, 'Ошибка Kinopoisk, проверьте правильность заполнения файла')

            if a3[0:24:1] == 'https://ru.wikipedia.org' or a3[0:24:1] == 'None':
                self.entry2.insert(0, a3)
            else:
                self.entry2.insert(0, 'Ошибка Wikipedia, проверьте правильность заполнения файла')

            if a4[0:19:1] == 'https://myseria.vip' or a4[0::1] == 'None':
                self.entry3.insert(0, a4)
            else:
                self.entry3.insert(0, 'Ошибка SerialFan, проверьте правильность заполнения файла')

            if a5[0:24:1] == 'https://h1.lordfilm.film' or a5[0:24:1] == 'https://ve.lordfilm.film' or a5[0:24:1] == 'None':
                self.entry4.insert(0, a5)
            else:
                self.entry4.insert(0, 'Ошибка LordFilm, проверьте правильность заполнения файла')

            if a6[14:28:1] == 'zetfix.online/' or a6[0:24:1] == 'None':
                self.entry5.insert(0, a6)
            else:
                self.entry5.insert(0, 'Ошибка ZetFlix, проверьте правильность заполнения файла')

            if a7[0:22:1] == 'https://www.tvigle.ru/' or a7[0:24:1] == 'None':
                self.entry6.insert(0, a7)
            else:
                self.entry6.insert(0, 'Ошибка Tvigle, проверьте правильность заполнения файла')

            if a8[0:24:1] == 'https://hd.kinopoisk.ru/' or a8[0:24:1] == 'None':
                self.entry7.insert(0, a8)
            else:
                self.entry7.insert(0, 'Ошибка KinopoiskHD, проверьте правильность заполнения файла')

            if a9[0:24:1] == 'https://multfilms.online' or a9[0:24:1] == 'None':
                self.entry8.insert(0, a9)
            else:
                self.entry8.insert(0, 'Ошибка MultFilm, проверьте правильность заполнения файла')
            write.write(a1)
            write.write(a2 + '\n')
            write.write(a3 + '\n')
            write.write(a4 + '\n')
            write.write(a5 + '\n')
            write.write(a6 + '\n')
            write.write(a7 + '\n')
            write.write(a8 + '\n')
            write.write(a9 + '\n')
            write.close()
            read.close()
            read = open('input.txt', 'r', encoding='utf-8')
            strings = read.readlines()
            read.close()
            cache = open('cache.txt', 'w', encoding='utf-8')
            for i in range(9, len(strings)):
                cache.write(strings[i])
            cache.close()
            os.remove('input.txt')
            os.rename('cache.txt', 'input.txt')

            # Парсинг
            global vision
            url_kino = self.entry1.get()
            url_wiki = self.entry2.get()
            url_serial = self.entry3.get()
            url_lord = self.entry4.get()
            url_zet = self.entry5.get()
            url_tvigle = self.entry6.get()
            url_hd = self.entry7.get()
            url_mult = self.entry8.get()

            if url_serial == '':
                url_serial = 'None'
            if url_lord == '':
                url_lord = 'None'
            if url_zet == '':
                url_zet = 'None'
            if url_tvigle == '':
                url_tvigle = 'None'
            if url_hd == '':
                url_hd = 'None'
            if url_mult == '':
                url_mult = 'None'

            if self.entry1.get() != '' and self.entry2.get() != '':
                results = prs.main(url_kino, url_wiki, url_serial, url_lord, url_zet, url_tvigle, url_hd, url_mult)
                a = '0'
                if results:
                    dsc = results[5]
                    if dsc != None:
                        a = dsc.find('\n')
                    if a == '0':
                        pass
                    else:
                        dsc = dsc.replace('\n', ' ')
                    self.text_area.configure(state='normal', wrap='none')
                    self.text_area.delete("0.0", 'end')
                    self.text_area.insert("0.0", f"✨ID: {results[0]}\n✨Name: {results[1]}\n"
                                                 f"✨Genre: {results[7]}\n✨Year: {results[4]}\n"
                                                 f"✨Season: {results[8]}\n✨Seria: {results[9]}\n"
                                                 f"✨Img: {results[2]}\n✨Kinopoisk: {results[10]}\n"
                                                 f"✨SerialFan: {results[11]}\n✨LordFilm: {results[12]}\n"
                                                 f"✨Wikipedia: {results[13]}\n✨ZetFlix: {results[14]}\n"
                                                 f"✨Tvigle: {results[15]}\n✨KinopoiskHD: {results[16]}\n"
                                                 f"✨MultFilm: {results[17]}\n✨Description: {dsc}\n"
                                                 f"✨Rating: {results[3]}\n✨Country: {results[6]}")
                    self.write(results[1])

            # Запись в БД
            import sqlite3
            db = sqlite3.connect("database\\database.db")
            cur = db.cursor()

            text = self.text_area.get("0.0", "end")
            text2 = text.split('\n')
            print(len(text2))
            if len(text2) != 19:
                self.button6.configure(text='Error len text', fg_color='#BD2C2C', hover_color='#7E1818')
                return
            else:
                self.button6.configure(text='Save',
                                       fg_color=color1, hover_color=color2)
            text = text.replace("\n", "").split("✨")
            text = text[1:]
            sel_list = []
            sel_list.append(text[0][4::1])
            sel_list.append(text[1][6::1])
            sel_list.append(text[2][7::1])
            sel_list.append(text[3][6::1])
            sel_list.append(text[4][8::1])

            sel_list.append(text[5][7::1])

            sel_list.append(text[6][5::1])
            sel_list.append(text[7][11::1])
            sel_list.append(text[8][11::1])
            sel_list.append(text[9][10::1])
            sel_list.append(text[10][11::1])
            sel_list.append(text[11][9::1])
            sel_list.append(text[12][8::1])
            sel_list.append(text[13][13::1])
            sel_list.append(text[14][10::1])
            sel_list.append(text[15][13::1])
            sel_list.append(text[16][8::1])
            sel_list.append(text[17][9::1])
            for item in sel_list:
                print(item)

            # Добавление в БД
            cur.execute("""INSERT INTO database VALUES (?, ?, ?, ?, ?, ?)""",
                        (sel_list[0], sel_list[1], sel_list[2], sel_list[3], sel_list[4], sel_list[5]))
            cur.execute("""INSERT INTO filminfo VALUES (?, ?, ?, ?, ?, ?)""",
                        (sel_list[0], sel_list[1], sel_list[6], sel_list[15], sel_list[16], sel_list[17]))
            cur.execute("""INSERT INTO urlbase VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (sel_list[0], sel_list[1], sel_list[7], sel_list[8], sel_list[9], sel_list[10], sel_list[11],
                         sel_list[12], sel_list[13], sel_list[14]))
            print('\nДанные записаны')
            db.commit()
            db.close()

    def copy(self):
        source_path = os.path.join("data", "url.txt")
        destination_path = "input.txt"
        print('\nНачат процесс копирования файла url в корневую папку')

        try:
            if os.path.exists(destination_path) and os.path.getsize(destination_path) > 34:
                with open('input.txt', 'r', encoding='utf-8') as f:
                    text = f.readlines()
                print(f"Файл 'input.txt' уже существует и заполнен на {len(text)} строк(и)\nЕсли вы уверены в "
                      f"копировании нажмите сочетание клавиш: 'Ctrl + W + E' для принудительного копирования")
            else:
                shutil.copy(source_path, destination_path)
                print("Файл успешно скопирован и переименован.")
        except FileNotFoundError:
            print("Файл не найден.")
        except Exception as e:
            print("Произошла ошибка:", e, '')

    def prinud_copy(self):
        source_path = os.path.join("data", "url.txt")
        destination_path = "input.txt"
        print('\nНачат процесс принудительного копирования файла url в корневую папку')

        try:
            shutil.copy(source_path, destination_path)
            print("Файл успешно скопирован и переименован.")
        except FileNotFoundError:
            print("Файл не найден.")
        except Exception as e:
            print("Произошла ошибка:", e)


    def delete(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow()
        else:
            self.toplevel_window.focus()

if __name__ == "__main__":
    app = App()
    app.mainloop()


