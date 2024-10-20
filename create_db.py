import sqlite3

con = sqlite3.connect('data.db')
cursor = con.cursor()


def create_db(klass):
    cursor.execute(f"""CREATE TABLE {klass}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                   )
                """)


def add_colum(klass):
    with open('data.txt', 'r', encoding='utf-8') as file:
        date = file.read().split('\n')

    for i in date:
        cursor.execute(f"ALTER TABLE {klass} ADD COLUMN date_{i.replace('.', '_')} INTEGER DEFAULT 'None'")
    con.commit()


def add_user(klass):
    with open('data.txt', 'r', encoding='utf-8') as file:
        date = file.read().split('\n')
    for user in date:
        cursor.execute(f"""
        INSERT INTO {klass} (name) VALUES (?)
        """, [user])
    con.commit()
#create_db('UR_11')
#add_colum('UR_11')
add_user('UR_11')
