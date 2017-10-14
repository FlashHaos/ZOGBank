#!/usr/bin/python
# -*- coding: utf-8 -*-
import random, string, hashlib
import sql

def generate_pw(length=8):
    password=""
    while len(password)<length:
        pwd = []
        pwd.append(random.choice(string.ascii_lowercase))
        pwd.append(random.choice(string.ascii_uppercase))
        pwd.append(str(random.randint(0,9)))
        random.shuffle(pwd)
        password+=pwd[0]
    return password

def get(id=False):
    conn = sql.connect()
    if not conn:
        return False
    if id:
        pass
    else:
        users=[]
        result=conn.cursor().execute("SELECT id, login, role FROM users").fetchall()
        for row in result:
            id, login, role=row
            users.append({'id':id, 'login':login, 'role':role})

def post(input):
    if not input['login']:
        return ({'error':'Login must be provided'},400)
    if input['login'] in ([x['login'] for x in users]):
        return ({'error':'Login must be unique'},400)
    if not input['password']:
        input['password']=generate_pw()
    input['id']=max([x['id'] for x in users])+1
    newuser={}
    newuser['id']=input['id']
    newuser['login']=input['login']
    newuser['passwordhash']=hashlib.md5(input['password'].encode('utf-8')).hexdigest()
    newuser['role']='user'
    users.append(newuser)
    return (input,201)

def delete(id):
    users=[x for x in users if x['id'] != id]
    return True

def login(username,passwordhash):
    for item in users:
        if item['login']==username:
            if item['passwordhash']==passwordhash:
                return item['id']
    return False