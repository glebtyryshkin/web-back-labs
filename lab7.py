from flask import Blueprint, render_template, request, abort, jsonify, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path


lab7 = Blueprint('lab7', __name__)

def db_connect():

    if current_app.config.get('DB_TYPE', 'postgres') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='gleb_tyryshkin_knowledge_base',
            user='gleb_tyryshkin_knowledge_base',
            password='glebtyryshkin'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # SQLite надо доделать
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def validate_film(film):
    errors = {}
    
    if not film.get('title_ru'):
        errors['title_ru'] = 'Заполните русское название!'
    

    year = film.get('year')
    if not year or not (1895 <= int(year) <= 2025):
        errors['year'] = 'Укажите год от 1895 до 2025'

    desc = film.get('description', '')
    if not desc:
        errors['description'] = 'Заполните описание!'
    elif len(desc) > 2000:
        errors['description'] = 'Описание слишком длинное'

    return errors

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    # Сортируем по ID, чтобы порядок не прыгал
    cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if film is None:
        return abort(404)
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    if film.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400
    
    if film.get('title', '') == '':
        film['title'] = film.get('title_ru')

    errors = validate_film(film)
    if errors:
        return errors, 400
    
    conn, cur = db_connect()
    
    # Сначала проверяем, есть ли фильм с таким ID
    cur.execute("SELECT id FROM films WHERE id = %s", (id,))
    if cur.fetchone() is None:
        db_close(conn, cur)
        return abort(404)

    cur.execute("""
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s
        WHERE id = %s
        RETURNING *
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    
    updated_film = cur.fetchone()
    db_close(conn, cur)
    
    return jsonify(updated_film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    if film.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400

    if film.get('title', '') == '':
        film['title'] = film.get('title_ru')

    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (film['title'], film['title_ru'], film['year'], film['description']))
    
    new_id = cur.fetchone()['id']
    db_close(conn, cur)
    
    # Возвращаем ID как объект, чтобы JS мог его прочитать
    return {'id': new_id}, 201
