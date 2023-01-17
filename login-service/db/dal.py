import sqlite3
from faker import Faker
#for testing 
ADMIN_USER="admin"
ADMIN_PASSWORD="admin"

class DAL:
    count=0
    filename="users.db"
    con=None # singleton design pattern (https://refactoring.guru/design-patterns/singleton)
    cur=None
    def __init__(self):
        if DAL.count==0:
            DAL.con=sqlite3.connect(DAL.filename,check_same_thread=False)
            DAL.cur=DAL.con.cursor()
            DAL.count+=1
    
    def initialize(self):
        DAL.con.execute('CREATE TABLE IF NOT EXISTS users ("username" TEXT,"password" TEXT)')
        DAL.con.commit()

    def authenticate(self,username,password):
        DAL().cur.execute(f'SELECT rowid,username,password FROM users WHERE (username="{username}" AND password="{password}")')
        res=DAL().cur.fetchall()
        if res:
            user_id=res[0][0]
        else:
            user_id='null'
        return user_id
    

class User:
    def __init__(self,username,password):
        self.username=username
        self.password=password

    def authenticate(self):
        self.user_id=DAL().authenticate(self.username,self.password)
        return self.user_id
    
    def save(self):
        DAL().cur.execute(f'INSERT INTO users(username,password) VALUES("{self.username}","{self.password}")')
        DAL().con.commit()
        
