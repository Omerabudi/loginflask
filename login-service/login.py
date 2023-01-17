from flask import Flask,Response,request
app = Flask(__name__)
import json
from db.dal import ADMIN_PASSWORD, DAL,User





@app.route('/login', methods=['POST']) 
def login():
    username=request.json["username"]
    password=request.json["password"]
    r=Response(json.dumps({'id':User(username,password).authenticate()}))
    r.headers['Content-type']='application/json'
    return r

@app.route('/register', methods=['POST']) 
def register():
    username=request.json["username"]
    password=request.json["password"]
    a=input("register user?(yes/no): ")
    try:
        if a=="yes":
            User(username,password).save()
            r=Response(json.dumps({'id':User(username,password).authenticate()}))
            r.headers['Content-type']='application/json'
        else:
            r=Response(json.dumps({'status':'null'}))
            r.headers['Content-type']='application/json'
        return r
    except:
        r=Response(json.dumps({'status':'null'}))
        r.headers['Content-type']='application/json'
        return r




@app.route('/add',methods=['POST']) 
def add_user():
    username=request.json["username"]
    password=request.json["password"]
    try:
        if ADMIN_PASSWORD==request.json["admin_pass"]:
            User(username,password).save()
            rs=DAL().cur.execute(f'SELECT * FROM users WHERE username="{username}"')
            if len(list(rs))>0:
                    user_id=User(username,password).authenticate()
                    r=Response(json.dumps({'status':'OK','user_id':user_id}))
                    DAL().con.commit()
                    r.headers['Content-type']='application/json'
                    return r
        else:
            r=Response(json.dumps({'status':'null'}))
            r.headers['Content-type']='application/json'
            return r
    except:           
            r=Response(json.dumps({'status':'null'}))
            r.headers['Content-type']='application/json'
            return r


@app.route('/remove',methods=['POST']) 
def remove_user():
    user_id=request.json["user_id"]
    rs=DAL().cur.execute(f'SELECT * FROM users WHERE rowid="{user_id}"')
    try:
        if len(list(rs))>0 and ADMIN_PASSWORD==request.json["admin_pass"]:
            DAL().cur.execute(f'DELETE FROM users WHERE rowid="{user_id}"')
            r=Response(json.dumps({'status':'OK'}))
        else:
            r=Response(json.dumps({'status':'Fail'}))
        r.headers['Content-type']='application/json'
        DAL().con.commit()
        return r
    except:
        r=Response(json.dumps({'status':'Fail'}))
        r.headers['Content-type']='application/json'
        return r


@app.route('/update', methods=['POST'])
def update_user():
    user_id=request.json["user_id"]
    password=request.json["password"]
    new_pass=request.json["new_pass"]
    rs=DAL().cur.execute(f'SELECT * FROM users WHERE rowid="{user_id}" AND password="{password}"')
    try:
        if len(list(rs))>0:
            DAL().cur.execute(f'UPDATE users SET password="{new_pass}" WHERE password="{password}"')
            r=Response(json.dumps({'status':'OK'}))
        else:
            r=Response(json.dumps({'status':'Fail'}))
        r.headers['Content-type']='application/json'
        DAL().con.commit()
        return r
    except:
        r=Response(json.dumps({'status':'Fail'}))
        r.headers['Content-type']='application/json'
        return r


@app.route('/list', methods=['GET']) 
def user_list():
    DAL().initialize() 
    rs=DAL().cur.execute('SELECT username FROM users')
    a=list(rs)
    if len(list(a))>0:
        r=Response(json.dumps({'status':'OK','username list':list(a)}))
    else:
        r=Response(json.dumps({'status':'Fail'}))
    r.headers['Content-type']='application/json'
    return r

@app.route('/list_all', methods=['POST']) 
def user_list_all():
    DAL().initialize() 
    rs=DAL().cur.execute('SELECT rowid,username FROM users')
    a=list(rs)
    try:
        if len(list(a))>0 and ADMIN_PASSWORD==request.json["admin_pass"]:
            r=Response(json.dumps({'status':'OK','id/username list':list(a)}))
        else:
            r=Response(json.dumps({'status':'Fail'}))
        r.headers['Content-type']='application/json'
        return r
    except:
        r=Response(json.dumps({'status':'Fail'}))
        r.headers['Content-type']='application/json'
        return r


if __name__ == '__main__':
    app.run(debug=True)

