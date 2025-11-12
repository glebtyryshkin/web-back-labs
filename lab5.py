from flask import Blueprint, render_template, request, redirect, session, current_app

import sqlite3

from os import path

import psycopg2

from psycopg2.extras import RealDictCursor

from werkzeug.security import generate_password_hash, check_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')

def lab():
    return render_template('lab5/lab5.html', login = session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'gleb_tyryshkin_knowledge_base',
            user = 'gleb_tyryshkin_knowledge_base',
            password = 'glebtyryshkin'
        )

        cur = conn.cursor(cursor_factory= RealDictCursor)

    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])

def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля!')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', 
                               error='Пользователь с таким логином уже существует!')

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, password) VALUES (%s, %s)",
            (login, password_hash))
    else:
        cur.execute(
            "INSERT INTO users (login, password) VALUES (?, ?)",
            (login, password_hash)
)



    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])

def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните все поля!')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        cur.close()
        conn.close()
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    session['login'] = login 
    cur.close()
    conn.close()
    return render_template('lab5/succes_login.html', login=login)
    
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_artricle.html')
    
    title = request.form.get('title')
    article_test = request.form.get('article_test')
    article_text = article_test

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, )) 

    user = cur.fetchone()
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        try:
            cur.execute(
                "INSERT INTO articles (user_id, title, article_test) VALUES (%s, %s, %s)",
                (user_id, title, article_test)
            )
        except:
            cur.execute(
                "INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)",
                (user_id, title, article_test)
            )
    else:
        try:
            cur.execute(
                "INSERT INTO articles (user_id, title, article_test) VALUES (?, ?, ?)",
                (user_id, title, article_test)
            )
        except:
            cur.execute(
                "INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?)",
                (user_id, title, article_test)
            )

    
    db_close(conn, cur)
    return redirect ('/lab5')

@lab5.route('/lab5/list')

def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, )) 
    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s;", (user_id, ))
    else:
        cur.execute(
            "SELECT * FROM articles WHERE user_id=?;", (user_id, )
        )
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template ('lab5/articles.html', articles=articles)

