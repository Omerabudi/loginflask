# for testing only

from faker import Faker
import sqlite3
con=sqlite3.connect('users.db')
cur=con.cursor()


def create_mock_users(user_num=20):
    users={}
    for i in range(user_num):
        username=Faker().profile()["username"]
        password=Faker().password()
        users[username]=password
        cur.execute(f'INSERT INTO users VALUES ("{username}","{password}")')
        con.commit()
    return users


def initizalize():
    cur.execute('CREATE TABLE IF NOT EXISTS users ("Username" TEXT,"Password" TEXT)')
    create_mock_users()

initizalize()