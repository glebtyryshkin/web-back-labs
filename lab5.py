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
def column_exists(cur, db_type, table, column):
    if db_type == 'postgres':
        cur.execute("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name=%s AND column_name=%s;
        """, (table, column))
        return cur.fetchone() is not None
    else:
        cur.execute(f"PRAGMA table_info({table});")
        rows = cur.fetchall()
        # sqlite Row: rows is list of rows where row[1] is name
        return any((r['name'] if isinstance(r, dict) else r[1]) == column for r in rows)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_artricle.html')

    title = request.form.get('title')
    # читаем оба варианта формы (на случай, если где-то остался старый шаблон)
    article_text = request.form.get('article_text') or request.form.get('article_test')

    if not title or not article_text:
        return render_template('lab5/create_artricle.html', error='Заполните все поля!')

    conn, cur = db_connect()

    # получаем id пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    user_id = user['id']

    # выбираем, в какую колонку писать — prefer article_text
    dbt = current_app.config.get('DB_TYPE') or 'sqlite'
    if column_exists(cur, dbt, 'articles', 'article_text'):
        col = 'article_text'
    elif column_exists(cur, dbt, 'articles', 'article_test'):
        col = 'article_test'
    else:
        # если ни одной колонки нет — создаём article_text (Postgres требует отдельного запроса, тут простой вариант)
        if dbt == 'postgres':
            cur.execute("ALTER TABLE articles ADD COLUMN article_text TEXT;")
        else:
            cur.execute("ALTER TABLE articles ADD COLUMN article_text TEXT;")
        col = 'article_text'

    if dbt == 'postgres':
        cur.execute(f"INSERT INTO articles (user_id, title, {col}) VALUES (%s, %s, %s);",
                    (user_id, title, article_text))
    else:
        cur.execute(f"INSERT INTO articles (user_id, title, {col}) VALUES (?, ?, ?);",
                    (user_id, title, article_text))

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')

    user_id = user['id']

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY id DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY id DESC;", (user_id,))
    raw_articles = cur.fetchall()
    db_close(conn, cur)

    articles = []
    for a in raw_articles:
        a_dict = dict(a)
        text = a_dict.get('article_text') or a_dict.get('article_test') or ''
        a_dict['article_text'] = text
        articles.append(a_dict)

    return render_template('lab5/articles.html', articles=articles)


