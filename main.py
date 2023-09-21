# import os
import re
import sqlite3

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto , LabeledPrice

from configs import *
from queries import *
from keyboards import *
from get_loc_name import *
from photos import input_media_group_photos, input_group_photos

# from photos_profiles import *

bot = TeleBot(TOKEN, parse_mode="HTML")

# ------------------------------------------------------------------------
users_data = {}
admin_data = {}
admin_enter = {}


# -------------------------------------------------------------------------
# Старт
@bot.message_handler(commands=['start'])
def command_start(message: Message):
    global users_data
    chat_id = message.chat.id
    users = get_all_users()
    admin = get_all_admins()
    if chat_id == ADMIN_ID:
        if chat_id in admin:
            greeting_admin(message)
        # else:
        # ask_full_name_admin(message)
        # login_admin(message)
    elif chat_id in users:
        main_menu(message)
    else:
        users_data[chat_id] = {
            "chat_id": chat_id
        }
        bot.send_message(chat_id, f'''<b>Приветсвуем Вас в нашем боте 😁
Для начала давайте пройдем регистрацию 📋</b>''',
                         reply_markup=ReplyKeyboardRemove())
        ask_full_name(message)


# -----------------------------------------------------------------------------------------------

@bot.message_handler(commands=get_login())
def command_login(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите кодовое слово''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, check_pass)


def check_pass(message: Message):
    if message.text == get_password():
        greeting_admin(message)


# ----------------------------------------------------------------------------------------------
# Регистрация Админа

# def ask_full_name_admin(message: Message):
#     chat_id = message.chat.id
#     admin_data[chat_id] = {
#         "chat_id": chat_id
#     }
#     msg = bot.send_message(chat_id, f"""<b>Напишите нам ваше имя или никнейм: 👤</b>""",
#                            reply_markup=ReplyKeyboardRemove())
#     bot.register_next_step_handler(msg,save_full_name_admin)
#
#
# def save_full_name_admin(message: Message):
#     global admin_data
#     chat_id = message.chat.id
#     full_name = message.text
#     admin_data[chat_id].update({"full_name": full_name})
#     ask_send_photo_for_profile_admin(message)
#
# def ask_send_photo_for_profile_admin(message: Message):
#     chat_id = message.chat.id
#     msg = bot.send_message(chat_id, f'''<b>Отпавьте вашу фотографию для анкеты вашего профиля 🖼</b>''',
#                            reply_markup=ReplyKeyboardRemove())
#     bot.register_next_step_handler(msg, save_profile_photo_admin)
#
#
# def save_profile_photo_admin(message: Message):
#     global admin_data
#     chat_id = message.chat.id
#     profile_photo = message.photo[0].file_id
#     insert_user_profile_photo_id(chat_id, profile_photo)
#     admin_data[chat_id].update({"profile_photo": profile_photo})
#     ask_phone_number_admin(message)
#
#
# def ask_phone_number_admin(message: Message):
#     chat_id = message.chat.id
#     msg = bot.send_message(chat_id,
#                            f"""<b>Отправьте ваш номер телефона: 📱</b>""",
#                            reply_markup=generate_btn_send_contact())
#     bot.register_next_step_handler(msg, save_phone_number_admin)
#
#
# def save_phone_number_admin(message: Message):
#     global admin_data
#     chat_id = message.chat.id
#     if message.content_type == 'text':
#         phone_number = message.text
#         if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
#             phone_number = message.text
#             admin_data[chat_id].update({"phone_number": phone_number})
#             print(admin_data)
#             login_admin(message)
#         else:
#             bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌</b>""")
#             ask_phone_number_admin(message)
#     elif message.content_type == 'contact':
#         phone_number = message.contact.phone_number
#         if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
#             phone_number = message.contact.phone_number
#             admin_data[chat_id].update({"phone_number": phone_number})
#             print(admin_data)
#             login_admin(message)
#         else:
#             bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌</b>""")
#             ask_phone_number_admin(message)
#
# # ------------------------------------------------------------------------------------------------
#
# def login_admin(message: Message):
#     chat_id = message.chat.id
#     msg = bot.send_message(chat_id, f'''Введите логин для входа: ''',
#                            reply_markup=ReplyKeyboardRemove())
#     bot.register_next_step_handler(msg, save_login_admin)
#
#
# def save_login_admin(message: Message):
#     chat_id = message.chat.id
#     login = message.text
#     admin_data[chat_id].update({"login": login})
#     print(admin_data)
#     password_admin(message)
#
# def password_admin(message: Message):
#     chat_id = message.chat.id
#     msg = bot.send_message(chat_id, f'''Введите пароль #️⃣: ''')
#     bot.register_next_step_handler(msg, save_password_admin)
#
# def save_password_admin(message: Message):
#     chat_id = message.chat.id
#     password = message.text
#     admin_data[chat_id].update({"password": password})
#     # logpass(message)
#     check_admin_data(message)
# # ------------------------------------------------------------------------------------------------
# def logpass(message: Message):
#     chat_id = message.chat.id
#     database = sqlite3.connect('bot_database.db')
#     cursor = database.cursor()
#     cursor.execute('''
#     INSERT INTO logpass(telegram_id, login, password)
#             VALUES (?,?,?)
#         ''' ,(chat_id,admin_data[chat_id]['login'], admin_data[chat_id]['password']))
#     database.commit()
#     database.close()
#
#
#
#
#
# # ------------------------------------------------------------------------------------------------
#
# def check_admin_data(message: Message):
#     global admin_data
#     chat_id = message.chat.id
#     bot.send_message(chat_id, f"""<b>Подтвердите ваши данные: 📋
# ----------------------------------------------------</b>""", reply_markup=ReplyKeyboardRemove())
#     bot.send_photo(chat_id, admin_data[chat_id]['profile_photo'], caption=f"""<b>
# Имя админа: {admin_data[chat_id]["full_name"]} 👤
# Номер телефона: {admin_data[chat_id]["phone_number"]} 📱
# Логин админа: {admin_data[chat_id]['login']}🤩
# Пароль админа: {admin_data[chat_id]['password']}#️⃣</b>""",
#                    reply_markup=generate_inline_yes_no())
#
#
# # -----------------------------------------------------------------------------------
#
# @bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
# def submit_admin_data(call: CallbackQuery):
#     global admin_data
#     chat_id = call.message.chat.id
#     if call.data == 'yes':
#         bot.delete_message(chat_id, call.message.message_id)
#         # ------------------------------------------------------------
#         database = sqlite3.connect("bot_database.db")
#         cursor = database.cursor()
#         cursor.execute("""
#             INSERT INTO admin(telegram_id, full_name,profile_photo, phone_number, login, password)
#             VALUES (?,?,?,?,?,?)
#         """, (chat_id,
#               admin_data[chat_id]["full_name"],
#               admin_data[chat_id]['profile_photo'],
#               admin_data[chat_id]["phone_number"],
#               admin_data[chat_id]["login"],
#               admin_data[chat_id]["password"]))
#         database.commit()
#         database.close()
#         # ------------------------------------------------------------
#         bot.send_message(chat_id, f"""Поздравляем 🎉🎉🎉
# Регистрация успешно пройдена ✅, теперь вы настоящий админ 🤴""")
#         greeting_admin(call.message)
#         admin_data = get_admin_profile_data(chat_id)
#         bot.send_photo(CHANNEL_ID, photo=admin_data[3], caption=f'''<b>
# Имя нового пользователя: {admin_data[2]}
# его номер телефона: {admin_data[4]}</b>''')
#
#     elif call.data == 'no':
#         bot.delete_message(chat_id, call.message.message_id)
#         admin_data.pop(chat_id)
#         bot.send_message(chat_id, f"""Регистрация прервано 📋❌""")
#         command_start(call.message)


# -----------------------------------------------------------------------------------------------

# Имя или никнейм пользователя
def ask_full_name(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Напишите нам ваше имя или никнейм: 👤</b>""")
    bot.register_next_step_handler(msg, save_full_name)


def save_full_name(message: Message):
    global users_data
    chat_id = message.chat.id
    full_name = message.text
    users_data[chat_id].update({"full_name": full_name})
    ask_send_photo_for_profile(message)


# --------------------------------------------------------------------------------------
# Аватарка(фото) пользователя
def ask_send_photo_for_profile(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''<b>Отпавьте вашу фотографию для анкеты вашего профиля 🖼</b>''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_profile_photo)


def save_profile_photo(message: Message):
    global users_data
    chat_id = message.chat.id
    profile_photo = message.photo[0].file_id
    insert_user_profile_photo_id(chat_id, profile_photo)
    users_data[chat_id].update({"profile_photo": profile_photo})
    ask_phone_number(message)


# ---------------------------------------------------------------------------------------
# Номер пользователя
def ask_phone_number(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           f"""<b>Отправьте ваш номер телефона: 📱</b>""",
                           reply_markup=generate_btn_send_contact())
    bot.register_next_step_handler(msg, save_phone_number)


def save_phone_number(message: Message):
    global users_data
    chat_id = message.chat.id
    if message.content_type == 'text':
        phone_number = message.text
        if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
            phone_number = message.text
            users_data[chat_id].update({"phone_number": phone_number})
            print(users_data)
            check_user_data(message)
        else:
            bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌📱 
Введите номер телефона (+998001234567) формата </b>""")
            ask_phone_number(message)
    elif message.content_type == 'contact':
        phone_number = message.contact.phone_number
        if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
            phone_number = message.contact.phone_number
            users_data[chat_id].update({"phone_number": phone_number})
            print(users_data)
            check_user_data(message)
        else:
            bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌📱</b>""")
            ask_phone_number(message)


# ----------------------------------------------------------------------------------------

# Проверка данных пользователя
def check_user_data(message: Message):
    global users_data
    chat_id = message.chat.id
    bot.send_message(chat_id, f"""<b>Подтвердите ваши данные: 📋
----------------------------------------------------</b>""", reply_markup=ReplyKeyboardRemove())
    bot.send_photo(chat_id, users_data[chat_id]['profile_photo'], caption=f"""<b>
Имя пользователя: {users_data[chat_id]["full_name"]} 👤
Номер телефона: {users_data[chat_id]["phone_number"]} 📱</b>""",
                   reply_markup=generate_inline_yes_no())


# -----------------------------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def submit_user_data(call: CallbackQuery):
    chat_id = call.message.chat.id
    if call.data == 'yes':
        bot.delete_message(chat_id, call.message.message_id)
        # ------------------------------------------------------------
        database = sqlite3.connect("bot_database.db")
        cursor = database.cursor()
        cursor.execute("""
            INSERT INTO users(telegram_id, full_name,profile_photo, phone_number)
            VALUES (?,?,?,?)
        """, (chat_id,
              users_data[chat_id]["full_name"],
              users_data[chat_id]['profile_photo'],
              users_data[chat_id]["phone_number"]))
        database.commit()
        database.close()
        # ------------------------------------------------------------
        bot.send_message(chat_id, f"""Поздравляем 🎉🎉🎉
Регистрация успешно пройдена ✅""")

        user_data = get_user_profile_data(chat_id)
        bot.send_photo(CHANNEL_ID, photo=user_data[3], caption=f'''<b>
Имя нового пользователя: {user_data[2]}
его номер телефона: {user_data[4]}</b>''')
        command_start(call.message)
    elif call.data == 'no':
        bot.delete_message(chat_id, call.message.message_id)
        users_data.pop(chat_id)
        bot.send_message(chat_id, f"""Регистрация прервана 📋❌""")
        command_start(call.message)


# --------------------------------------------------------------------

# MAIN FUNCTIONS

# Меню пользователя
def main_menu(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Выберите что делать: 📋</b>""",
                           reply_markup=generate_main_menu_buttons())
    bot.register_next_step_handler(msg, check_user_action)


def check_user_action(message: Message):
    if message.text == 'Мой профиль👤':
        Profile(message)
    elif message.text == 'Украшения 💎':
        ask_category_products(message)
    elif message.text == 'Оставить отзыв ✍':
        ask_feedback(message)


# ---------------------------------------------------------------------

def product(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'''<b>Выберите товар который Вас интересует 💎</b>''')


# ---------------------------------------------------------------------
# Профиль пользователя
def Profile(message: Message):
    global users_data
    chat_id = message.chat.id
    user_data = get_user_profile_data(chat_id)
    bot.send_photo(chat_id, photo=user_data[3], caption=f'''<b>
     Имя пользователя: {user_data[2]}
Номер телефона: {user_data[4]}</b>''', reply_markup=generate_profile_buttons())
    check_profile_action(message)


# --------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text in ["Изменить фотографию профиля📷",
                                                           "Изменить имя пользователя👤",
                                                           "Изменить номер телефона 📱",
                                                           "Удалить профиль пользователя❌",
                                                           'Назад 🔙'])
def check_profile_action(message: Message):
    if message.text == "Изменить фотографию профиля📷":
        change_photo__profile(message)
    elif message.text == "Изменить имя пользователя👤":
        change_name(message)
    elif message.text == "Изменить номер телефона 📱":
        change_phone_number(message)
    elif message.text == "Удалить профиль пользователя❌":
        delete_profile(message)
    elif message.text == 'Назад 🔙':
        main_menu(message)


# Профиль админа

def Admins_profile(message: Message):
    global admin_data
    chat_id = message.chat.id
    admin_data = get_admin_profile_data(chat_id)
    bot.send_photo(chat_id, photo=admin_data[3], caption=f'''<b>
     Имя администратора: {admin_data[2]}
Номер телефона: {admin_data[4]}
логин администратора: {admin_data[5]}
кодовое слово: {admin_data[6]} </b>''', reply_markup=generate_admins_profile_buttons())
    check_admin_profile_action(message)


@bot.message_handler(func=lambda message: message.text in ["Изменить фотографию админа 📷",
                                                           "Изменить имя админа 🤴",
                                                           "Изменить номер админа 📱",
                                                           "Удалить профиль админа ❌",
                                                           "Измениить логин 🤠",
                                                           "Изменить пароль 🔐",
                                                           'Назад в меню 🔙'])
def check_admin_profile_action(message: Message):
    if message.text == "Изменить фотографию админа 📷":
        change_admin_photo(message)
    elif message.text == "Изменить имя админа 🤴":
        change_admin_name(message)
    elif message.text == "Изменить номер админа 📱":
        change_admin_phone_number(message)
    elif message.text == "Удалить профиль админа ❌":
        delete__admin_profile(message)
    elif message.text == 'Измениить логин 🤠':
        change_login(message)
    elif message.text == "Изменить пароль 🔐":
        change_password(message)
    elif message.text == 'Назад в меню 🔙':
        greeting_admin(message)


# -----------------------------------------------------------------------------
# Смена имени или никнейма админа
def change_admin_name(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите новое имя или никнейм админа : ''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_admins_name_change)


def save_admins_name_change(message: Message):
    chat_id = message.chat.id
    new_name = message.text
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE  admin
        SET full_name = ?
        WHERE telegram_id = ?
        """, (new_name, chat_id))
    database.commit()
    database.close()
    Admins_profile(message)


# ------------------------------------------------------------------------------
# Смена аватарки админа

def change_admin_photo(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''<b>Отпавьте новую фотографию для анкеты вашего профиля 🖼</b>''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_admins_photo_change)


def save_admins_photo_change(message: Message):
    chat_id = message.chat.id
    new_photo = message.photo[0].file_id
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE  admin
        SET profile_photo = ?
        WHERE telegram_id = ?
        """, (new_photo, chat_id))
    database.commit()
    database.close()
    Admins_profile(message)


# ------------------------------------------------------------------------------
# Смена номера админа


def change_admin_phone_number(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите новый номер телефона : ''',
                           reply_markup=generate_btn_send_contact())
    bot.register_next_step_handler(msg, change_admins_phone)


def change_admins_phone(message: Message):
    chat_id = message.chat.id
    if message.content_type == 'text':
        phone_number = message.text
        if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
            new_phone_number = message.text
            database = sqlite3.connect("bot_database.db")
            cursor = database.cursor()
            cursor.execute("""
                    UPDATE  admin
                    SET phone_number = ?
                    WHERE telegram_id = ?
                    """, (new_phone_number, chat_id))
            database.commit()
            database.close()
            Admins_profile(message)

        else:
            bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌📱</b>""")
            change_admin_phone_number(message)

    elif message.content_type == 'contact':
        phone_number = message.contact.phone_number
        if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
            new_phone_number = message.contact.phone_number
            database = sqlite3.connect("bot_database.db")
            cursor = database.cursor()
            cursor.execute("""
                                UPDATE  admin
                                SET phone_number = ?
                                WHERE telegram_id = ?
                                """, (new_phone_number, chat_id))
            database.commit()
            database.close()
            Admins_profile(message)
        else:
            bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌📱</b>""")
            change_admin_phone_number(message)


# ------------------------------------------------------------------------------
# Удаления профиля админа

def delete__admin_profile(message: Message):
    chat_id = message.chat.id
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
            DELETE  FROM admin
            WHERE telegram_id = ?
            """, (chat_id,))
    database.commit()
    database.close()
    command_start(message)


# ------------------------------------------------------------------------------
# Смена логина

def change_login(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите новый логин: ''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_login_change)


def save_login_change(message: Message):
    chat_id = message.chat.id
    new_login = message.text
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE admin
        SET login = ?
        WHERE telegram_id = ?
        """, (new_login, chat_id))
    database.commit()
    database.close()
    Admins_profile(message)


# ------------------------------------------------------------------------------
# Смена пароля


def change_password(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите новый логин: ''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_password_change)


def save_password_change(message: Message):
    chat_id = message.chat.id
    new_login = message.text
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE admin
        SET password = ?
        WHERE telegram_id = ?
        """, (new_login, chat_id))
    database.commit()
    database.close()
    Admins_profile(message)


# -------------------------------------------------------------------------------
# Смена имени или никнейма пользователя
def change_name(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите новое имя пользователя : ''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_name_change)


def save_name_change(message: Message):
    chat_id = message.chat.id
    new_name = message.text
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE  users
        SET full_name = ?
        WHERE telegram_id = ?
        """, (new_name, chat_id))
    database.commit()
    database.close()
    Profile(message)


# def check_name_change(message: Message):
#     chat_id = message.chat.id
#     user_data = get_user_profile_photo(chat_id)
#     bot.send_message(chat_id, f"""<b>Подтвердите ваши изменения : 📋
#     ----------------------------------------------------</b>""", reply_markup=ReplyKeyboardRemove())
#     bot.send_message(chat_id, f'''{user_data[2]}''',
#                      reply_markup=generate_inline_yes_no())


# @bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
# def save_name_change(call: CallbackQuery):
#     chat_id = call.message.chat.id
#     new_name = call.message.text
#     if call.data == 'yes':
#         database = sqlite3.connect("bot_database.db")
#         cursor = database.cursor()
#         cursor.execute("""
#                 UPDATE  users
#                 SET full_name = ?
#                 WHERE telegram_id = ?
#                 """, (new_name, chat_id))
#         database.commit()
#         database.close()
#         # ------------------------------------------------------------
#         bot.send_message(chat_id, f"""Поздравляем 🎉🎉🎉
# имя пользователя успешно изменено ✅🙂""")
#     elif call.data == 'no':
#         bot.send_message(chat_id, f"""Изменения имени пользователя прервано 📋❌""")
#         command_start(call.message)

# ----------------------------------------------------------------------
# Смена номера
def change_phone_number(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''Введите новый номер телефона : ''',
                           reply_markup=generate_btn_send_contact())
    bot.register_next_step_handler(msg, change_phone)


def change_phone(message: Message):
    chat_id = message.chat.id
    if message.content_type == 'text':
        phone_number = message.text
        if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
            new_phone_number = message.text
            database = sqlite3.connect("bot_database.db")
            cursor = database.cursor()
            cursor.execute("""
                    UPDATE  users
                    SET phone_number = ?
                    WHERE telegram_id = ?
                    """, (new_phone_number, chat_id))
            database.commit()
            database.close()
            Profile(message)

        else:
            bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌📱</b>""")
            change_phone_number(message)

    elif message.content_type == 'contact':
        phone_number = message.contact.phone_number
        if re.match(r'([+]?)998([3789])([01345789])\d{7}', phone_number):
            new_phone_number = message.contact.phone_number
            database = sqlite3.connect("bot_database.db")
            cursor = database.cursor()
            cursor.execute("""
                                UPDATE  users
                                SET phone_number = ?
                                WHERE telegram_id = ?
                                """, (new_phone_number, chat_id))
            database.commit()
            database.close()
            Profile(message)
        else:
            bot.send_message(chat_id, f"""<b>Вы ввели не корректный номер телефона ❌📱</b>""")
            change_phone_number(message)


# ----------------------------------------------------------------------
# Смена картинки
def change_photo__profile(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'''<b>Отпавьте новую фотографию для анкеты вашего профиля 🖼</b>''',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_photo_change)


def save_photo_change(message: Message):
    chat_id = message.chat.id
    new_photo = message.photo[0].file_id
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE  users
        SET profile_photo = ?
        WHERE telegram_id = ?
        """, (new_photo, chat_id))
    database.commit()
    database.close()
    Profile(message)


# ----------------------------------------------------------------------
# Удаление профиля
def delete_profile(message: Message):
    chat_id = message.chat.id
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
            DELETE  FROM users
            WHERE telegram_id = ?
            """, (chat_id,))
    database.commit()
    database.close()
    command_start(message)


# ----------------------------------------------------------------------
# Локация
def menu(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Отправьте локацию: 📍</b>""",
                           reply_markup=generate_location_buttons())
    bot.register_next_step_handler(msg, check_user_loc_answer)


def check_user_loc_answer(message: Message):
    chat_id = message.chat.id
    if message.text == "Мои адреса 🗺":
        msg = bot.send_message(chat_id, f"""<b>Выберите адрес доставки: 🗺</b>""",
                               reply_markup=generate_user_addresses(chat_id))
        bot.register_next_step_handler(msg, check_user_address)
    elif message.text == "Назад ⬅":
        main_menu(message)
    elif message.content_type == "location":
        latitude = message.location.latitude
        longitude = message.location.longitude
        loc_name = get_location_name(latitude, longitude)
        msg = bot.send_message(chat_id, f"""<b>Подтвердите адрес доставки:
{loc_name}</b>""",
                               reply_markup=generate_submit_location_buttons())
        bot.register_next_step_handler(msg, check_user_location, loc_name, latitude, longitude)


def check_user_location(message: Message, location, latitude, longitude):
    chat_id = message.chat.id
    if message.text == "Назад ⬅":
        menu(message)
    elif message.text == "Нет ❌":
        menu(message)
    elif message.text == "Да ✅":
        save_user_location(chat_id, location, latitude, longitude)
        ask_category_products(message)


# ----------------------------------------------------------------
def check_user_address(message: Message):
    chat_id = message.chat.id
    if message.text == "Назад ⬅":
        menu(message)
    else:
       ask_category_products(message)


# ----------------------------------------------------------------
# def ask_category(message: Message):
#     chat_id = message.chat.id
#     msg = bot.send_message(chat_id, f"""<b>Выберите категорию: </b>""",
#                            reply_markup=generate_categories_buttons())
#     bot.register_next_step_handler(msg, show_products)


# ----------------------------------------------------------------
# def show_products(message: Message):
#     chat_id = message.chat.id
#     if message.text == "Назад ⬅":
#         main_menu(message)
#     elif message.text in get_all_categories():
#         category_name = message.text
#         bot.send_message(chat_id, f"""<b>Вы выбрали категорию: {category_name}</b>""")
#         category_id = get_category_id(category_name)
#         bot.send_media_group(chat_id, input_media_group_photos(category_id))
#         msg = bot.send_message(chat_id, f"""<b>Выберите товар: </b>""",
#                                reply_markup=generate_products_buttons(category_name))


# --------------------------------------------------------------------

def ask_category_products(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Выберите категорию: </b>""",
                           reply_markup=generate_categories_buttons())
    bot.register_next_step_handler(msg, show_my_products)


# Товары
def show_my_products(message: Message):
    chat_id = message.chat.id
    if message.text == "Назад ⬅":
        main_menu(message)
    elif message.text == 'Корзина 🛒':
        show_cart(message)
    elif message.text in get_all_categories():
        category = message.text
        bot.send_message(chat_id, f"""<b>Вы выбрали категорию: {category}</b>""",
                         reply_markup=generate_products_buttons(category))
        category_id = get_category_id(category)
        bot.send_media_group(chat_id, input_group_photos(category_id))
        msg = bot.send_message(chat_id, f"""<b>Выберите товар: </b>""")
        bot.register_next_step_handler(msg, product_detail)


# --------------------------------------------------------------------

def product_detail(message: Message):
    chat_id = message.chat.id
    if message.text == "Назад ⬅":
        ask_category_products(message)
    # elif message.text == 'Корзина 🛒':
    #     show_cart(message)
    else:
        product_name = message.text
        product_data = get_product_data(product_name)
        with open(product_data[5], mode='rb') as img:
            bot.send_message(chat_id, f'''<b>Выберите одно из следующих: </b>''',
                             reply_markup=generate_cart_back())
            msg = bot.send_photo(chat_id, img, caption=f'''<b>Название:{product_data[1]}
==============================
Описание : {product_data[2]}
==============================
Цена: {product_data[3]}  сум</b>''',
                                 reply_markup=generate_pagination_buttons(product_data[0]))
            bot.register_next_step_handler(msg, check_user_product)


def check_user_product(message: Message):
    if message.text == 'Назад ⬅':
        ask_category_products(message)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    # elif message.text == 'Корзина 🛒':
    #     show_cart(message)


# --------------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: "cart" in call.data)
def add_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split("_")
    product_id, quantity = int(product_id), int(quantity)
    # -----------------------------------------------------------------
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    # -----------------------------------------------------------------
    cursor.execute("""
    SELECT user_id FROM users
    WHERE telegram_id = ?
    """, (chat_id,))
    user_id = cursor.fetchone()[0]
    # -----------------------------------------------------------------
    try:
        cursor.execute("""SELECT cart_id FROM carts WHERE user_id = ?""", (user_id,))
        cart_id = cursor.fetchone()[0]
    except:
        cursor.execute("""INSERT INTO carts(user_id) VALUES (?)""", (user_id,))
        database.commit()
        cursor.execute("""SELECT cart_id FROM carts WHERE user_id = ?""", (user_id,))
        cart_id = cursor.fetchone()[0]

    cursor.execute("""
    SELECT product_price, product_name
    FROM products WHERE product_id = ?
    """, (product_id,))

    price, product_name = cursor.fetchone()
    final_price = quantity * int(price)

    try:
        cursor.execute("""
            INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
            VALUES (?,?,?,?)
        """, (cart_id, product_name, quantity, final_price))
        bot.answer_callback_query(call.id, f"{product_name} {quantity} штуки добавлено в корзину !")
        database.commit()

        bot.delete_message(chat_id, message_id=call.message.message_id)
        ask_category(call.message)

    except:
        cursor.execute("""SELECT quantity, final_price FROM cart_products
        WHERE cart_id = ? AND product_name = ?""", (cart_id, product_name))
        old_quantity, old_final_price = cursor.fetchone()
        old_quantity, old_final_price = int(old_quantity), int(old_final_price)
        old_quantity += int(quantity)
        old_final_price += int(final_price)
        cursor.execute("""
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE cart_id = ? AND product_name = ?
        """, (old_quantity, old_final_price, cart_id, product_name))
        database.commit()
        bot.answer_callback_query(call.id, f"""{product_name} {quantity} штуки добавлено в корзину !""")

        bot.delete_message(chat_id, message_id=call.message.message_id)
        ask_category_products(call.message)





# --------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Корзина 🛒')
def show_cart(message: Message, edit_message:bool = False):
    chat_id = message.chat.id
    database = sqlite3.connect('bot_database.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
        SELECT user_id FROM users WHERE telegram_id = ?
        ''', (chat_id, ))
        user_id = cursor.fetchone()[0]
        cursor.execute('''
        SELECT cart_id FROM carts WHERE user_id = ?
        ''', (user_id, ))
        cart_id = cursor.fetchone()[0]
        try:
            cursor.execute('''
            UPDATE carts
            SET total_products = (SELECT SUM(quantity) FROM cart_products
            WHERE cart_id = :cart_id),
            total_price = (SELECT SUM(final_price) FROM cart_products
            WHERE cart_id = :cart_id)
            WHERE cart_id = :cart_id
            ''',{'cart_id': cart_id})
            database.commit()
        except:
            bot.send_message(chat_id, f'Ваша корзина пуста !')
            database.close()
            ask_category_products(message)
        cursor.execute('''SELECT total_products, total_price
        FROM carts WHERE user_id = ?''', (user_id, ))
        total_products, total_price = cursor.fetchone()
        total_price = float(total_price)


        cursor.execute('''SELECT product_name, quantity, final_price
        FROM cart_products WHERE cart_id = ?''',(cart_id, ))
        cart_products = cursor.fetchall()

        text = f'Ваша корзина: \n'
        i = 0

        for product_name, quantity, final_price in cart_products:
            i += 1
            text += f'''{i}. {product_name}
Количество: {quantity}
Цена: {final_price}\n\n'''
        text += f'''Общее число товаров: {0 if total_products is None else total_products}
Общая цена: {0 if total_price is None else total_price}
Доставка: 20000 сум \n
Итого: {total_price + 20000} сум'''

        if edit_message:
            bot.edit_message_text(text, chat_id, message.message_id,
                                  reply_markup=generate_cart_inline(cart_id))
        else:
            bot.send_message(chat_id, f'Проверьте вашу корзину !',
                             reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id, text, reply_markup=generate_cart_inline(cart_id))
    except:
        bot.send_message(chat_id,f'''Ваша корзина пуста !''')
        bot.delete_message(chat_id,message.message_id)
        ask_category_products(message)
        database.close()
        return

# --------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: 'delete' in call.data)
def delete_product_cart(call: CallbackQuery):
    message = call.message

    _, cart_product_id = call.data.split('_')
    cart_product_id = int(cart_product_id)
    database = sqlite3.connect('bot_database.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products
    WHERE cart_product_id = ?
    ''',(cart_product_id, ))

    database.commit()
    database.close()
    bot.answer_callback_query(call.id, f'Продукт успешно удален !')

    show_cart(message,edit_message=True)


@bot.callback_query_handler(func=lambda call: 'back' in call.data)
def back_to_categories(call: CallbackQuery):
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, message_id)
    ask_category_products(call.message)




# --------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: 'change' in call.data)
def change_quantity(call: CallbackQuery):
    chat_id = call.message.chat.id

    _, product_id, quantity = call.data.split('_')
    product_id, quantity = int(product_id), int(quantity)
    message_id = call.message.message_id
    if quantity > 0:
        bot.edit_message_reply_markup(chat_id, message_id,
                                      reply_markup=generate_pagination_buttons(product_id, quantity))





@bot.callback_query_handler(func=lambda call: 'clear' in call.data)
def clear_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    database = sqlite3.connect('bot_database.db')
    cursor = database.cursor()
    cursor.execute('''
            SELECT user_id FROM users WHERE telegram_id = ?
            ''', (chat_id,))
    user_id = cursor.fetchone()[0]
    cursor.execute('''
            SELECT cart_id FROM carts WHERE user_id = ?
            ''', (user_id,))
    cart_id = cursor.fetchone()[0]

    cursor.execute('''
    DELETE FROM cart_products WHERE cart_id = ?
    ''', (cart_id, ))
    database.commit()
    cursor.execute('''DELETE FROM carts WHERE cart_id = ?''',(cart_id, ))
    database.commit()
    database.close()

    bot.send_message(chat_id, f'''Ваша корзина очищена !''')
    bot.delete_message(chat_id, message_id=call.message.message_id)
    main_menu(call.message)



@bot.callback_query_handler(lambda call: 'order' in call.data)
def make_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)
    database = sqlite3.connect('bot_database.db')
    cursor = database.cursor()


    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''',(cart_id, ))
    cart_products = cursor.fetchall()

    cursor.execute('''SELECT total_products, total_price FROM carts
    WHERE cart_id = ?''', (cart_id, ))
    total_products, total_price = cursor.fetchone()
    total_price = int(total_price)

    text = f'''Ваш чек: \n\n'''
    i = 0
    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f'''{i}. {product_name}
Количество: {quantity}
Цена {total_price}\n\n'''

    text += f'''Итоговая цена : {0 if total_price is None else total_price}'''

    bot.send_invoice(
        chat_id= chat_id,
        title=f'Чек № {cart_id}',
        description=text,
        invoice_payload='bot-defined invoice payload',
        provider_token='371317599:TEST:1686228677115',
        currency='UZS',
        prices=[
            LabeledPrice(label='Общая цена', amount=int(str(total_price)+ '00')),
            LabeledPrice(label='Доставка', amount=2000000)
        ]
    )







# --------------------------------------------------------------------
# Отзывы
def ask_feedback(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Отправьте ваш отзыв: 📱</b>""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_feedback)


def save_feedback(message: Message):
    chat_id = message.chat.id
    feedback = message.text
    bot.send_message(chat_id, f"""<b>Спасибо за ваш отзыв ✅</b>""")
    bot.send_message(CHANNEL_ID, f"""<b>Отзыв от клиента: ✅
--------------------------
{feedback}</b>""")
    main_menu(message)


# ----------------------------------------------------------------------------
# Админ
def greeting_admin(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"""<b>Добро пожаловать админ !</b>""",
                     reply_markup=generate_admin_buttons())


@bot.message_handler(func=lambda message: message.text in ["Профиль админа 🤴",
                                                           "Количество пользователей 👥",
                                                           "Рассылка 📮"])  # and message.chat.id == ADMIN_ID)
def check_admin_action(message: Message):
    chat_id = message.chat.id
    admin = get_admin_profile_data(chat_id)
    if message.text == 'Профиль админа 🤴':
        if chat_id in admin:
            Admins_profile(message)
        # else:
        #     ask_full_name_admin(message)
    elif message.text == "Количество пользователей 👥":
        users_quantity(message)
    elif message.text == "Рассылка 📮":
        check_mailing_type(message)
        bot.send_message(chat_id, f'''Выберите что разослать 🗳''', reply_markup=generate_mailing_buttons())


# ---------------------------------------------------------------------------

def users_quantity(message: Message):
    chat_id = message.chat.id
    database = sqlite3.connect('bot_database.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT telegram_id FROM users
    ''')
    users = cursor.fetchall()
    users__quantity = []
    for user in users:
        users__quantity.append(user)
    msg = bot.send_message(chat_id, f'''<b> Количество пользователей: {len(users__quantity)} </b>''',
                           reply_markup=back())
    bot.register_next_step_handler(msg, check_back)
    return msg


def check_back(messange: Message):
    if messange.text == 'Назад в меню 🔙':
        return greeting_admin(messange)


# ----------------------------------------------------------------------------
# Рассылка
@bot.message_handler(func=lambda message: message.text in ["Текст 📝", "Картинка 🖼", "Видео 🎞",
                                                           "Картинка 🖼 + Текст 📝",
                                                           "Видео 🎞 + Текст 📝",
                                                           "Назад в меню 🔙"])  # and message.chat.id == ADMIN_ID)
def check_mailing_type(message: Message):
    if message.text == "Текст 📝":
        ask_text_for_mailing(message)
    elif message.text == "Картинка 🖼":
        ask_image_for_mailing(message)
    elif message.text == "Видео 🎞":
        ask_video_for_mailing(message)
    elif message.text == "Картинка 🖼 + Текст 📝":
        ask_image_text_for_mailing(message)
    elif message.text == "Видео 🎞 + Текст 📝":
        ask_video_text_for_mailing(message)
    elif message.text == "Назад в меню 🔙":
        greeting_admin(message)


# ---------------------------------------------------------------------------------------------------
# Текстовая рассылка
def ask_text_for_mailing(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Напишите текст для рассылки: 📝</b>""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, submit_text_for_mailing)


def submit_text_for_mailing(message: Message):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, f"""<b>Подтвердите рассылку вашего текста : 📝
=======================================

{text}</b>""",
                           reply_markup=generate_yes_no())
    bot.register_next_step_handler(msg, check_answer_for_mailing_text, text)


def check_answer_for_mailing_text(message: Message, text):
    if message.text == "Да ✅":
        user_ids = get_all_users()
        for user in user_ids:
            try:
                bot.send_message(user, f"""{text}""")
            except:
                pass
        greeting_admin(message)

    elif message.text == "Нет ❌":
        greeting_admin(message)


# ---------------------------------------------------------------------------------------------------
# Рассылка картинок
def ask_image_for_mailing(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Отправьте фото для рассылки: 🖼</b>""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, submit_image_for_mailing)


def submit_image_for_mailing(message: Message):
    chat_id = message.chat.id
    image = message.photo[-1].file_id
    msg = bot.send_photo(chat_id, photo=image,
                         caption=f"""<b>Подтвердите рассылку вашего фото : 🖼</b>""",
                         reply_markup=generate_yes_no())
    bot.register_next_step_handler(msg, check_answer_for_mailing_photo, image)


def check_answer_for_mailing_photo(message: Message, image):
    if message.text == "Да ✅":
        user_ids = get_all_users()
        for user in user_ids:
            try:
                bot.send_photo(user, image)
            except:
                pass
        greeting_admin(message)

    elif message.text == "Нет ❌":
        greeting_admin(message)


# ------------------------------------------------------------------------------
# Рассылка видео
def ask_video_for_mailing(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Отправьте video для рассылки: </b>""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, submit_video_for_mailing)


def submit_video_for_mailing(message: Message):
    chat_id = message.chat.id
    video = message.video.file_id
    msg = bot.send_video(chat_id, video=video,
                         caption=f"""<b>Подтвердите рассылку вашего video: </b>""",
                         reply_markup=generate_yes_no())
    bot.register_next_step_handler(msg, check_answer_for_mailing_video, video)


def check_answer_for_mailing_video(message: Message, video):
    if message.text == "Да ✅":
        user_ids = get_all_users()
        for user in user_ids:
            try:
                bot.send_video(user, video)
            except:
                pass
        greeting_admin(message)

    elif message.text == "Нет ❌":
        greeting_admin(message)


# ----------------------------------------------------------------------------
# Рассылка картинок с описанием
def ask_image_text_for_mailing(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""Отправьте фото для рассылки: 🖼""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, mailing_text_photo)


def mailing_text_photo(message: Message):
    chat_id = message.chat.id
    photo = message.photo[-1].file_id
    msg = bot.send_message(chat_id, f"Введите текст для описание фото: 📝")
    bot.register_next_step_handler(msg, check_mailing_photo_text, photo)


def check_mailing_photo_text(message: Message, photo):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_photo(chat_id, photo, caption=text,
                         reply_markup=generate_yes_no())
    bot.register_next_step_handler(msg, submit_mailing_photo_text, photo, text)


def submit_mailing_photo_text(message: Message, photo, text):
    if message.text == "Да ✅":
        tg_ids = get_all_users()
        for user in tg_ids:
            bot.send_photo(user, photo, caption=text)
        greeting_admin(message)
    elif message.text == "Нет ❌":
        greeting_admin(message)


# -------------------------------------------------------------------------------
# Рассылка видео с описанием
def ask_video_text_for_mailing(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""Отправьте видео для рассылки: 🎞""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, mailing_text_video)


def mailing_text_video(message: Message):
    chat_id = message.chat.id
    video = message.video.file_id
    msg = bot.send_message(chat_id, f"Введите текст для описание video: 🎞")
    bot.register_next_step_handler(msg, check_mailing_video_text, video)


def check_mailing_video_text(message: Message, video):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_video(chat_id, video, caption=text,
                         reply_markup=generate_yes_no())
    bot.register_next_step_handler(msg, submit_mailing_video_text, video, text)


def submit_mailing_video_text(message: Message, video, text):
    if message.text == "Да ✅":
        tg_ids = get_all_users()
        for user in tg_ids:
            bot.send_video(user, video, caption=text)
        greeting_admin(message)
    elif message.text == "Нет ❌":
        greeting_admin(message)


# ------------------------------------------------------------------------------

@bot.message_handler(content_types=['photo'])
def photo_handler(message: Message):
    chat_id = message.chat.id
    photo = message.photo[-1].file_id
    print(photo)


# ------------------------------------------------------------------------------

bot.polling(none_stop=True, timeout=60)
