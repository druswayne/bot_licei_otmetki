import sqlite3
from datetime import datetime, timedelta
import random
import string
con = sqlite3.connect('data.db')
cursor = con.cursor()
month = {1:"янв",
         2:"фев",
         3:"мар",
         4:"апр",
         5:"май",
         6:"июн",
         7:"июл",
         8:"авг",
         9:"сен",
         10:"окт",
         11:"ноя",
         12:"дек",
}

def generate_token(length=10):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token


def create_table_day(klass):
    cursor.execute(f"""CREATE TABLE {klass}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                   )
                """)

def get_dates_excluding_days_and_dates(start_date, end_date, exclude_days, exclude_dates):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() not in exclude_days and current_date not in exclude_dates:
            date_list.append(current_date)
        current_date += timedelta(days=1)
    return date_list
def add_colum(klass,exclude_days):
    # Пример использования
    start_date = datetime(2024, 11, 4)
    end_date = datetime(2024, 12, 24)

    # 0 понедельник
    exclude_dates = {datetime(2024, 11, 7)}  # Исключаем конкретные даты

    dates = get_dates_excluding_days_and_dates(start_date, end_date, exclude_days, exclude_dates)
    for date in dates:
        date_ = f'date_{date.day:02}_{month[date.month]}'
        cursor.execute(f"ALTER TABLE {klass} ADD COLUMN {date_} INTEGER DEFAULT 'None'")
    con.commit()

add_colum('G_10', {5,6,4})
def add_user(klass, files):
    with open(files, 'r', encoding='utf-8') as file:
        date = file.read().split('\n')
    for user in date:
        cursor.execute(f"""
        INSERT INTO {klass} (name) VALUES (?)
        """, [user])
    con.commit()


def create_user_list():
    cursor.execute(f"""CREATE TABLE users
                    (name TEXT,
                    klass TEXT,
                    token TEXT
                   )
                """)


def add_user_list():
    token_list = []
    with open('data.txt', 'r', encoding='utf-8') as file:
        data_user = file.readlines()
    for user in data_user:
        print(user)
        data_user = user.replace('\n', '').split()
        name = f'{data_user[0]} {data_user[1]}'
        klass = data_user[2]
        token = generate_token()
        while token in token_list:
            token = generate_token()
        token_list.append(token)

        cursor.execute(f"""
                INSERT INTO users (name, klass, token) VALUES (?,?,?)
                """, (name, klass, token))
    con.commit()


from datetime import datetime, timedelta

def get_dates_excluding_days_and_dates(start_date, end_date, exclude_days, exclude_dates):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() not in exclude_days and current_date not in exclude_dates:
            date_list.append(current_date)
        current_date += timedelta(days=1)
    return date_list


# create_db('UR_11')
# add_colum('UR_11')
# add_user('UR_11')

#add_user('L_11', 'list_user_class.txt')