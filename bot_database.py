import hashlib
import sqlite3


def add_user_db(user_id):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()
        user_id = str(user_id)

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users_data(
            id TEXT NOT NULL PRIMARY KEY,
            access INT NOT NULL DEFAULT 0,
            code TEXT NOT NULL)
        ''')

        if not cur.execute('SELECT id FROM users_data WHERE id = ?', [user_id]).fetchone():
            cur.execute('INSERT INTO users_data(id, code) VALUES(?, ?)',
                        (user_id, hashlib.md5((user_id + 'md5').encode()).hexdigest()))


def check_access(user_id):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()

        return bool(cur.execute('SELECT access FROM users_data WHERE id = ?', [user_id]).fetchone()[0])


def access(user_id, code):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()

        if code == cur.execute('SELECT code FROM users_data WHERE id = ?', [user_id]).fetchone()[0]:
            cur.execute('UPDATE users_data SET access = 1 WHERE id = ?', [user_id])
