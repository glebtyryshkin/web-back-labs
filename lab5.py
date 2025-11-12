from flask import Blueprint, render_template, request, redirect, session, current_app, abort

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
    
@lab5.route('/lab5/logout')

def logout():
    session.pop('login', None)
    return redirect('/lab5/')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_artricle.html', article=None, action_url='/lab5/create', submit_text='Опубликовать')

    title = (request.form.get('title') or '').strip()
    article_text = (request.form.get('article_text') or '').strip()

    if not title or not article_text:
        return render_template('lab5/create_artricle.html', article={'title': title, 'article_text': article_text},
                               action_url='/lab5/create', submit_text='Опубликовать',
                               error='Тема и текст статьи не должны быть пустыми.')

    conn, cur = db_connect()
    db_type = current_app.config.get('DB_TYPE') or 'sqlite'

    # получаем id пользователя
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/login')
    user = dict(user_row)
    user_id = user.get('id')

    if db_type == 'postgres':
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);",
            (user_id, title, article_text)
        )
    else:
        cur.execute(
            "INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);",
            (user_id, title, article_text)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('DB_TYPE') or 'sqlite'

    # получаем id пользователя
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()

    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/login')

    user = dict(user_row)
    user_id = user.get('id')

    # выбираем статьи пользователя
    if db_type == 'postgres':
        cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY id DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY id DESC;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('DB_TYPE') or 'sqlite'

    # получаем id пользователя
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/login')
    user = dict(user_row)
    user_id = user.get('id')

    # получаем статью и проверяем владельца
    if db_type == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    row = cur.fetchone()
    if not row:
        db_close(conn, cur)
        return redirect('/lab5/list')

    article = dict(row)
    # колонка с автором может называться login_id или user_id — пробуем оба
    author_id = article.get('login_id') or article.get('user_id')
    if author_id != user_id:
        db_close(conn, cur)
        return abort(403)  # запрет на редактирование чужой статьи

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/create_artricle.html',
                               article={'title': article.get('title',''), 'article_text': article.get('article_text','')},
                               action_url=f'/lab5/edit/{article_id}',
                               submit_text='Сохранить')

    # POST — сохраняем изменения
    title = (request.form.get('title') or '').strip()
    article_text = (request.form.get('article_text') or '').strip()
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/create_artricle.html',
                               article={'title': title, 'article_text': article_text},
                               action_url=f'/lab5/edit/{article_id}',
                               submit_text='Сохранить',
                               error='Тема и текст статьи не должны быть пустыми.')

    if db_type == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


# Удаление статьи (POST)
@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('DB_TYPE') or 'sqlite'

    # получаем id пользователя
    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/login')
    user = dict(user_row)
    user_id = user.get('id')

    # проверяем статью и владельца
    if db_type == 'postgres':
        cur.execute("SELECT login_id, user_id FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT login_id, user_id FROM articles WHERE id=?;", (article_id,))
    row = cur.fetchone()
    if not row:
        db_close(conn, cur)
        return redirect('/lab5/list')
    article = dict(row)
    author_id = article.get('login_id') or article.get('user_id')
    if author_id != user_id:
        db_close(conn, cur)
        return abort(403)

    # удаляем
    if db_type == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')