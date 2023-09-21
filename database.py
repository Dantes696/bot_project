import sqlite3

database = sqlite3.connect("bot_database.db")
cursor = database.cursor()

def create_table_admin():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        full_name TEXT DEFAULT '',
        profile_photo TEXT,
        phone_number DEFAULT '',
        login TEXT DEFAULT 'mugiwara',
        password TEXT DEFAULT 'JopanOleg'
    );    
    ''')

create_table_admin()

def create_login_pass():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logpass(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        login TEXT DEFAULT 'mugiwara', 
        password TEXT DEFAULT 'касатка33' 
    );
    """)


create_login_pass()




def create_table_users():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        full_name TEXT DEFAULT '',
        profile_photo TEXT,
        phone_number DEFAULT ''
    );
    """)


create_table_users()


def create_locations_table():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations(
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_chat_id INTEGER,
        location_name TEXT UNIQUE,
        latitude TEXT,
        longitude TEXT
        )
        """)
    database.commit()
    database.close()


create_locations_table()

def create_categories_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE,
        category_photo TEXT
        )
        """)

create_categories_table()

def create_category_photos_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_photos(
            photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            photo TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(category_id)
            )
            """)

create_category_photos_table()
database.commit()
database.close()

def create_products_categories_table():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE,
        category_photo TEXT
        )
        """)
    database.commit()
    database.close()

create_products_categories_table()



def create_categories_table():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE,
        category_photo TEXT
        )
        """)

create_categories_table()

def create_category_photos_table():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_photos(
            photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            photo TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(category_id)
            )
            """)

create_category_photos_table()


def create_products_table():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        product_description TEXT,
        product_price TEXT,
        category_id INTEGER,
        product_photo TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    )
    """)

create_products_table()


def create_carts_table():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()

    query = """CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        total_products INTEGER DEFAULT 0,
        total_price TEXT DEFAULT 0
    )"""
    cursor.execute(query)


create_carts_table()


def create_carts_products():
    database = sqlite3.connect("bot_database.db")
    cursor = database.cursor()
    query = """CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        product_name TEXT,
        quantity TEXT,
        final_price TEXT,
        UNIQUE(cart_id, product_name)
    )"""
    cursor.execute(query)

    database.commit()
    database.close()


create_carts_products()
























