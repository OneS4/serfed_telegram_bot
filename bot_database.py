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


def new_left_del(group_id, switch, botname):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()
        group_id = str(group_id)

        cur.execute('''
            CREATE TABLE IF NOT EXISTS groups(
            id TEXT NOT NULL PRIMARY KEY,
            deleting_login_messages TEXT NOT NULL DEFAULT 'no',
            deleting_exit_messages TEXT NOT NULL DEFAULT 'no')
        ''')

        if not cur.execute('SELECT id FROM groups WHERE id = ?', [group_id]).fetchone():
            cur.execute('INSERT INTO groups(id) VALUES(?)', [group_id])

        if switch == f'/on_del_login{botname}':
            cur.execute("UPDATE groups SET deleting_login_messages = 'yes' WHERE id = ?", [group_id])
        elif switch == f'/on_del_exit{botname}':
            cur.execute("UPDATE groups SET deleting_exit_messages = 'yes' WHERE id = ?", [group_id])
        elif switch == f'/off_del_login{botname}':
            cur.execute("UPDATE groups SET deleting_login_messages = 'no' WHERE id = ?", [group_id])
        elif switch == f'/off_del_exit{botname}':
            cur.execute("UPDATE groups SET deleting_exit_messages = 'no' WHERE id = ?", [group_id])


def check_on_off_new_left_def(group_id, switch):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()
        group_id = str(group_id)

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS groups(
                    id TEXT NOT NULL PRIMARY KEY,
                    deleting_login_messages TEXT NOT NULL DEFAULT 'no',
                    deleting_exit_messages TEXT NOT NULL DEFAULT 'no')
                ''')

        if not cur.execute('SELECT id FROM groups WHERE id = ?', [group_id]).fetchone():
            cur.execute('INSERT INTO groups(id) VALUES(?)', [group_id])

        if switch == 'new_chat_members':
            if cur.execute('SELECT deleting_login_messages FROM groups WHERE id = ?', [group_id]).fetchone()[
                0] == 'yes':
                return True
        elif switch == 'left_chat_member':
            if cur.execute('SELECT deleting_exit_messages FROM groups WHERE id = ?', [group_id]).fetchone()[0] == 'yes':
                return True
        return False


def call_all(group_id, admins_list):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()
        group_id = '_' + str(group_id)[1:]

        cur.execute("CREATE TABLE IF NOT EXISTS " + group_id + "(user_id TEXT NOT NULL PRIMARY KEY)")

        for admin in admins_list:
            if not cur.execute('SELECT user_id FROM ' + group_id + ' WHERE user_id = ?', [admin]).fetchone():
                cur.execute('INSERT INTO ' + group_id + ' (user_id) VALUES(?)', [admin])
        user_list = list()
        for user in cur.execute('SELECT user_id FROM ' + group_id).fetchall():
            user_list.append(user[0])
        return user_list


def add_new_user_call_all(user_id, group_id):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()
        group_id = '_' + str(group_id)[1:]

        cur.execute("CREATE TABLE IF NOT EXISTS " + group_id + "(user_id TEXT NOT NULL PRIMARY KEY)")

        if not cur.execute('SELECT user_id FROM ' + group_id + ' WHERE user_id = ?', [user_id]).fetchone():
            cur.execute('INSERT INTO ' + group_id + ' (user_id) VALUES(?)', [user_id])

def delete_user_call_all(user_id, group_id):
    with sqlite3.connect('bot_data.db') as con:
        cur = con.cursor()
        group_id = '_' + str(group_id)[1:]

        cur.execute("CREATE TABLE IF NOT EXISTS " + group_id + "(user_id TEXT NOT NULL PRIMARY KEY)")

        if cur.execute('SELECT user_id FROM ' + group_id + ' WHERE user_id = ?', [user_id]).fetchone():
            cur.execute('DELETE FROM ' + group_id + ' WHERE user_id = ?', [user_id])
