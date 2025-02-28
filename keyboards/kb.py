from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from textbot import text_bot as tx

# Главное меню
kb1 = [[InlineKeyboardButton(text=tx.KB_MAIN_TEXT.btn1, callback_data="random_value"),
    InlineKeyboardButton(text=tx.KB_MAIN_TEXT.btn2, callback_data="generation_film")],
    [InlineKeyboardButton(text=tx.KB_MAIN_TEXT.btn3, callback_data="vision_films"),
    InlineKeyboardButton(text=tx.KB_MAIN_TEXT.btn4, callback_data="search_films")],
    [InlineKeyboardButton(text=tx.KB_MAIN_TEXT.btn5, callback_data="buy_films"),
    InlineKeyboardButton(text=tx.KB_MAIN_TEXT.btn6, callback_data="message_help")]]

# Меню помощи
kb2 = [[InlineKeyboardButton(text=tx.KB_HELP_TEXT.btn1, callback_data="help_random"),
    InlineKeyboardButton(text=tx.KB_HELP_TEXT.btn2, callback_data="help_generation")],
    [InlineKeyboardButton(text=tx.KB_HELP_TEXT.btn3, callback_data="help_vision"),
    InlineKeyboardButton(text=tx.KB_HELP_TEXT.btn4, callback_data="help_search")],
    [InlineKeyboardButton(text=tx.KB_HELP_TEXT.btn6, callback_data="main_menu2"),
     InlineKeyboardButton(text=tx.KB_HELP_TEXT.btn5, callback_data="help_buy")]]
kb3 = [[InlineKeyboardButton(text=tx.HELP_TEXT.header, callback_data="message_help")]]

#Меню подбора
kb4 = [[InlineKeyboardButton(text=tx.KB_RANDOM_TEXT.btn1, callback_data="random_genre"),
        InlineKeyboardButton(text=tx.KB_RANDOM_TEXT.btn2, callback_data="random_rating")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_TEXT.btn3, callback_data="random_country"),
        InlineKeyboardButton(text=tx.KB_RANDOM_TEXT.btn4, callback_data="random_year")],
        [InlineKeyboardButton(text=tx.KB_RANDOM_TEXT.btn5, callback_data="main_menu2")]]

#Меню подбора (1 страница)
kb5 = [[InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn1, callback_data="genre_select_боевик"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn2, callback_data="genre_select_детектив")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn3, callback_data="genre_select_фантастика"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn4, callback_data="genre_select_триллер")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn5, callback_data="genre_select_драма"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn6, callback_data="genre_select_комедия")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn7, callback_data="random_value"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE1_TEXT.btn8, callback_data="random_two")]]

#Меню подбора (2 страница)
kb6 = [[InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn1, callback_data="genre_select_документальный"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn2, callback_data="genre_select_история")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn3, callback_data="genre_select_биография"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn4, callback_data="genre_select_приключения")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn5, callback_data="genre_select_мультфильм"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn6, callback_data="genre_select_аниме")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn7, callback_data="random_genre"),
    InlineKeyboardButton(text=tx.KB_RANDOM_GENRE2_TEXT.btn8, callback_data="main_menu2")]]

kb7 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_genre"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_genre")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_genre"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="watching_films")]]


kb8 = [[InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn1, callback_data="country_select_США"),
    InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn2, callback_data="country_select_Франция")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn3, callback_data="country_select_Англия"),
    InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn4, callback_data="country_select_Россия")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn5, callback_data="country_select_Корея"),
    InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn6, callback_data="country_select_Япония")],
    [InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn7, callback_data="random_value"),
    InlineKeyboardButton(text=tx.KB_RANDOM_COUNTRY_TEXT.btn8, callback_data="main_menu2")]]


kb9 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_country"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_country")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_country"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="watching_films")]]

kb10 = [[InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn1, callback_data="year_select_2020"),
         InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn2, callback_data="year_select_2010")],
        [InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn3, callback_data="year_select_2000"),
         InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn4, callback_data="year_select_1990")],
        [InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn5, callback_data="year_select_1980"),
         InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn6, callback_data="year_select_1970")],
        [InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn7, callback_data="random_value"),
         InlineKeyboardButton(text=tx.KB_RANDOM_YEAR.btn8, callback_data="main_menu2")]]

kb11 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_year"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_year")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_year"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="watching_films")]]

kb12 = [[InlineKeyboardButton(text=tx.KB_RANDOM_RATING.btn1, callback_data="rating_select_9"),
         InlineKeyboardButton(text=tx.KB_RANDOM_RATING.btn2, callback_data="rating_select_8")],
        [InlineKeyboardButton(text=tx.KB_RANDOM_RATING.btn3, callback_data="rating_select_7"),
         InlineKeyboardButton(text=tx.KB_RANDOM_RATING.btn4, callback_data="rating_select_6")],
        [InlineKeyboardButton(text=tx.KB_RANDOM_RATING.btn5, callback_data="random_value"),
         InlineKeyboardButton(text=tx.KB_RANDOM_RATING.btn6, callback_data="main_menu2")]]
kb13 = [[InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn1, callback_data="back_film_rating"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn2, callback_data="next_film_rating")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn3, callback_data="random_rating"),
        InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn4, callback_data="add_favorit")],
       [InlineKeyboardButton(text=tx.KB_RANDOM_FILMS.btn5, callback_data="watching_films")]]


menu_kb1 = InlineKeyboardMarkup(inline_keyboard=kb1)
menu_kb2 = InlineKeyboardMarkup(inline_keyboard=kb2)
kb_help_text = InlineKeyboardMarkup(inline_keyboard=kb3)
menu_kb4 = InlineKeyboardMarkup(inline_keyboard=kb4)
menu_kb5 = InlineKeyboardMarkup(inline_keyboard=kb5)
menu_kb6 = InlineKeyboardMarkup(inline_keyboard=kb6)
menu_kb7 = InlineKeyboardMarkup(inline_keyboard=kb7)
menu_kb8 = InlineKeyboardMarkup(inline_keyboard=kb8)
menu_kb9 = InlineKeyboardMarkup(inline_keyboard=kb9)
menu_kb10 = InlineKeyboardMarkup(inline_keyboard=kb10)
menu_kb11 = InlineKeyboardMarkup(inline_keyboard=kb11)
menu_kb12 = InlineKeyboardMarkup(inline_keyboard=kb12)
menu_kb13 = InlineKeyboardMarkup(inline_keyboard=kb13)
