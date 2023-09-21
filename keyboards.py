import sqlite3

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from queries import get_user_loc_names, get_all_categories, get_all_products


def generate_btn_send_contact():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_send_contact = KeyboardButton(text="Отправить контакт 📱",
                                      request_contact=True)
    markup.add(btn_send_contact)
    return markup


def generate_inline_yes_no():
    markup = InlineKeyboardMarkup(row_width=2)
    btn_yes = InlineKeyboardButton(text="Да ✅", callback_data="yes")
    btn_no = InlineKeyboardButton(text="Нет ❌", callback_data="no")
    markup.add(btn_yes, btn_no)
    return markup


def generate_mailing_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn_text = KeyboardButton(text="Текст 📝")
    btn_image = KeyboardButton(text="Картинка 🖼")
    btn_video = KeyboardButton(text="Видео 🎞")
    btn_image_text = KeyboardButton(text="Картинка 🖼 + Текст 📝")
    btn_video_text = KeyboardButton(text="Видео 🎞 + Текст 📝")
    btn_back = KeyboardButton(text="Назад в меню 🔙")
    markup.row(btn_text, btn_image)
    markup.row(btn_video)
    markup.row(btn_image_text)
    markup.row(btn_video_text)
    markup.row(btn_back)

    return markup


def generate_yes_no():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_yes = KeyboardButton(text="Да ✅")
    btn_no = KeyboardButton(text="Нет ❌")
    markup.add(btn_yes, btn_no)
    return markup


def generate_main_menu_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_menu = KeyboardButton(text="Украшения 💎")
    btn_profile = KeyboardButton(text="Мой профиль👤")
    btn_feedback = KeyboardButton(text="Оставить отзыв ✍")
    # btn_back = KeyboardButton(text="Назад ⬅")
    markup.row(btn_menu)
    markup.row(btn_profile,btn_feedback)

    # markup.row(btn_back)
    return markup


def generate_location_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_locations = KeyboardButton(text="Мои адреса 🗺")
    btn_send_location = KeyboardButton(text="Отправить локацию 📍",
                                       request_location=True)
    btn_back = KeyboardButton(text="Назад ⬅")
    markup.row(btn_send_location)
    markup.row(btn_locations, btn_back)
    return markup


def generate_submit_location_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = KeyboardButton(text="Да ✅")
    btn_no = KeyboardButton(text="Нет ❌")
    btn_back = KeyboardButton(text="Назад ⬅")
    markup.row(btn_yes, btn_no)
    markup.row(btn_back)
    return markup


def generate_user_addresses(chat_id):
    addresses = get_user_loc_names(chat_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = []
    for address in addresses:
        btn = KeyboardButton(text=f"{address}")
        buttons.append(btn)

    markup.add(*buttons)
    markup.add(KeyboardButton(text="Назад ⬅"))
    return markup


def generate_categories_buttons():
    categories = get_all_categories()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=f"{category}")
        buttons.append(btn)

    markup.add(*buttons)

    markup.add(KeyboardButton(text='Корзина 🛒'))
    markup.add(KeyboardButton(text="Назад ⬅"))
    return markup

def generate_products_buttons(category_name):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    products = get_all_products(category_name)
    for product in products:
        btn = KeyboardButton(text=f"{product}")
        buttons.append(btn)

    markup.add(*buttons)

    markup.add(KeyboardButton(text="Назад ⬅"))
    return markup


def generate_profile_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    change_photo = KeyboardButton(text=f'''Изменить фотографию профиля📷''')
    change_f_n = KeyboardButton(text=f'''Изменить имя пользователя👤''')
    change_phone_number = KeyboardButton(text=f'''Изменить номер телефона 📱''')
    delete_profile = KeyboardButton(text=f'''Удалить профиль пользователя❌''')
    back = KeyboardButton(text=f'''Назад 🔙''')
    markup.row(change_photo,change_f_n)
    markup.row(change_phone_number ,delete_profile)
    markup.row(back)
    return markup

def generate_admins_profile_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    change_photo = KeyboardButton(text=f'''Изменить фотографию админа 📷''')
    change_f_n = KeyboardButton(text=f'''Изменить имя админа 🤴''')
    change_phone_number = KeyboardButton(text=f'''Изменить номер админа 📱 ''')
    delete_profile = KeyboardButton(text=f'''Удалить профиль админа ❌''')
    change_login = KeyboardButton(text=f'''Измениить логин 🤠''')
    change_pass = KeyboardButton(text=f'''Изменить пароль 🔐''')
    back = KeyboardButton(text=f'''Назад в меню 🔙''')
    markup.row(change_photo,change_f_n,change_phone_number)
    markup.row(change_login, change_pass,delete_profile)
    markup.row(back)
    return markup

def generate_admin_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    mailing = KeyboardButton(text=f'''Рассылка 📮''')
    how_many_users = KeyboardButton(text=f'''Количество пользователей 👥''')
    profile_admin = KeyboardButton(text=f'''Профиль админа 🤴''')
    markup.row(profile_admin)
    markup.row(mailing,how_many_users)
    return markup



def back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text=f'''Назад в меню 🔙''')
    markup.row(back)
    return markup



def generate_pagination_buttons(product_id , quantity=1):
    markup = InlineKeyboardMarkup()
    btn_minus = InlineKeyboardButton(text='➖',
                                     callback_data=f'change_{product_id}_{quantity-1}')
    btn_plus = InlineKeyboardButton(text='➕',
                                     callback_data=f'change_{product_id}_{quantity+1}')
    btn_quantity = InlineKeyboardButton(text=str(quantity), callback_data='quantity')
    add_to_cart = InlineKeyboardButton(text='Добавить в корзину 🛒',
                                       callback_data=f'cart_{product_id}_{quantity}')

    markup.row(btn_minus, btn_quantity, btn_plus)
    markup.row(add_to_cart)

    return markup

def generate_cart_back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    markup.add(KeyboardButton(text='Корзина 🛒'))
    markup.add(KeyboardButton(text='Назад ⬅'))


    return markup

def generate_cart_inline(cart_id):
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('Назад ⬅',callback_data='back')
    clear_cart = InlineKeyboardButton('Очистить корзину полностью 🛒', callback_data='clear')
    submit_order = InlineKeyboardButton('Оформить заказ 🚖',
                                        callback_data=f'order_{cart_id}')


    markup.row(submit_order)
    markup.row(clear_cart)
    markup.row(back)

    database = sqlite3.connect('bot_database.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_product_id, product_name
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id, ))

    cart_products = cursor.fetchall()
    database.close()

    for product_id , product_name in cart_products:
        markup.row(
            InlineKeyboardButton(text=f'❌ {product_name}', callback_data=f'delete_{product_id}')
        )
    return markup