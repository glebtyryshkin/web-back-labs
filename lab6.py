from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='gleb_tyryshkin_knowledge_base',
            user='gleb_tyryshkin_knowledge_base',
            password='glebtyryshkin'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
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

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html', current_user=session.get('login'))

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    # Получаем список всех офисов
    if data['method'] == 'info':
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices ORDER BY number;")
        offices = cur.fetchall()
        db_close(conn, cur)
        # Преобразуем offices для корректного вывода с SQLite
        offices = [dict(row) for row in offices]
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    # Проверка авторизации
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Unauthorized'},
            'id': id
        }

    # Бронирование офиса
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        query = "SELECT * FROM offices WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM offices WHERE number = ?"
        cur.execute(query, (office_number,))
        office = cur.fetchone()
        if not office:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': 3, 'message': 'Office not found'}, 'id': id}
        if office['tenant']:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': 2, 'message': 'Already booked'}, 'id': id}
        update_query = "UPDATE offices SET tenant = %s WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres' else "UPDATE offices SET tenant = ? WHERE number = ?"
        cur.execute(update_query, (login, office_number))
        db_close(conn, cur)
        return {'jsonrpc': '2.0', 'result': 'Booking successful', 'id': id}

    # Отмена бронирования
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        query = "SELECT * FROM offices WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM offices WHERE number = ?"
        cur.execute(query, (office_number,))
        office = cur.fetchone()
        if not office:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': 3, 'message': 'Office not found'}, 'id': id}
        if office['tenant'] != login:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': 4, 'message': 'Cannot cancel another user\'s booking'}, 'id': id}
        update_query = "UPDATE offices SET tenant = '' WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres' else "UPDATE offices SET tenant = '' WHERE number = ?"
        cur.execute(update_query, (office_number,))
        db_close(conn, cur)
        return {'jsonrpc': '2.0', 'result': 'Cancellation successful', 'id': id}

    # Неизвестный метод
    return {'jsonrpc': '2.0', 'error': {'code': -32601, 'message': 'Method not found'}, 'id': id}