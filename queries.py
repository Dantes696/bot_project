import sqlite3


def insert_user_telegram_id(chat_id: int) -> None:
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    INSERT INTO users(telegram_id)
    VALUES (?)
    """, (chat_id,))
    database.commit()
    database.close()


def insert_user_full_name(chat_id: int, full_name: str):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    UPDATE users
    SET full_name = ?
    WHERE telegram_id = ?
    """, (full_name, chat_id))
    database.commit()
    database.close()


def insert_user_profile_photo_id(chat_id: int, profile_photo: str):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    UPDATE users
    SET profile_photo = ?
    WHERE telegram_id = ?
    """, (profile_photo, chat_id))
    database.commit()
    database.close()


def insert_user_phone_number(chat_id: int, phone_number: str):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        UPDATE users
        SET phone_number = ?
        WHERE telegram_id = ?
        """, (phone_number, chat_id))
    database.commit()
    database.close()


def get_user_data(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT full_name, profile_photo , phone_number FROM users
    WHERE telegram_id = ?
    """, (chat_id,))
    user_data = cursor.fetchone()
    database.close()
    return user_data


def delete_user_data(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    DELETE FROM users
    WHERE telegram_id = ?
    """, (chat_id,))
    database.commit()
    database.close()


def get_all_users():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT telegram_id FROM users;
    """)
    telegram_id = cursor.fetchall()
    database.close()

    user_ids = []
    for user in telegram_id:
        user_ids.append(user[0])

    return user_ids

    # [(123456789,), (123789456,), (456789123,), ]
    # [123456789, 123789456, 456789123]


def save_user_location(user_id, location_name, latitude, longitude):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO locations(user_chat_id, location_name, latitude, longitude)
    VALUES (?,?,?,?)
    """, (user_id, location_name, latitude, longitude))
    database.commit()
    database.close()


def get_user_loc_names(chat_id):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT location_name FROM locations
    WHERE user_chat_id = ?
    """, (chat_id,))
    user_loc_names = cursor.fetchall()
    database.close()

    locations = [loc[0] for loc in user_loc_names]

    return locations


def get_all_categories():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT category_name FROM categories;
    """)
    categories = cursor.fetchall()
    database.close()

    categories_names = [cat[0] for cat in categories]

    return categories_names


def get_category_id(name):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT category_id FROM categories
    WHERE category_name =?
    """, (name,))
    category_id = cursor.fetchone()
    database.close()

    return category_id[0]


def get_category_photos(category_id):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT photo FROM category_photos
    WHERE category_id = ?
    """, (category_id,))
    category_photos = cursor.fetchall()
    database.close()

    photos = [cat[0] for cat in category_photos]

    return photos


# ---------------------------------------------------------------

def get_all_products(category_name):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT category_id  FROM categories
    WHERE category_name = ?
    """, (category_name,))
    category_id = cursor.fetchone()[0]

    cursor.execute('''
    SELECT product_name FROM products
    WHERE category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()

    product_names = [product[0] for product in products]

    return product_names


def get_products_id(name):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT product_id FROM products
    WHERE category_id = ?
    """, (name,))
    products_id = cursor.fetchone()
    database.close()

    return products_id


def get_product_photos(category_id):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT product_photo FROM products
    WHERE category_id = ?
    """, (category_id,))
    products_photos = cursor.fetchall()
    database.close()

    photos = [product[0] for product in products_photos]

    return photos


# ----------------------------------------------------------------
def get_user_profile_data(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT * FROM users
    WHERE telegram_id = ?
    """, (chat_id,))
    user_data = cursor.fetchone()  # (1, "Azamat Yaxyoyev", "+998901139933", "Photo")
    database.close()

    return user_data

    # return user_data


def get_user_profile_name(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT full_name FROM users
    WHERE telegram_id = ?
    """, (chat_id, ))
    user_data = cursor.fetchone()
    database.close()
    user_name = []
    for user in user_data:
        user_name.append(user)

    return user_name[0]


def get_user_profile_phone(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT phone_number FROM users
    WHERE telegram_id = ?
    """, (chat_id, ))
    user_data = cursor.fetchone()
    database.close()
    user_phone = []
    for user in user_data:
        user_phone.append(user)

    return user_phone[0]


def get_admin_profile_data(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT * FROM admin
    WHERE telegram_id = ?
    """, (chat_id,))
    admin_data = cursor.fetchone()

    return admin_data


def get_admins_data(chat_id: int):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT full_name, profile_photo , phone_number, login, password FROM admin
    WHERE telegram_id = ?
    """, (chat_id,))
    admin_data = cursor.fetchall()
    database.close()
    admin_ids = []
    for admin in admin_data:
        admin_ids.append(admin[0])

    return admin_data


def get_all_admins():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT telegram_id FROM users;
    """)
    telegram_id = cursor.fetchall()
    database.close()

    user_ids = []
    for user in telegram_id:
        user_ids.append(user[0])

    return user_ids


def get_password():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        SELECT password FROM admin;
        """)
    password = cursor.fetchone()
    database.close()

    admins_pass = []
    for p in password:
        admins_pass.append(p)

    return admins_pass[0]


def get_login():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        SELECT login FROM admin;
        """)
    login = cursor.fetchone()
    database.close()

    admins_log = []
    for p in login:
        admins_log.append(p)
    return admins_log[0]


def get_product_data(product_name):
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
          SELECT * FROM products
          WHERE product_name = ?         
    """, (product_name,))
    data = cursor.fetchone()

    database.close()
    return data
