from flask import Blueprint, render_template, request, jsonify, abort, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor

rgz = Blueprint('rgz', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='gleb_tyryshkin_knowledge_base',
        user='gleb_tyryshkin_knowledge_base',
        password='glebtyryshkin'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz/')
def index():
    # Передаем в шаблон информацию, админ ли сейчас на сайте
    # Допустим, админ - это пользователь с логином 'root'
    is_admin = session.get('login') == 'root' 
    return render_template('rgz/index.html', is_admin=is_admin)


@rgz.route('/rgz/api/books/', methods=['GET'])
def get_books():
    # 1. Сбор параметров
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    # Фильтры
    title_filter = request.args.get('title', '')
    author_filter = request.args.get('author', '')
    publisher_filter = request.args.get('publisher', '')
    pages_min = request.args.get('pages_min')
    pages_max = request.args.get('pages_max')
    
    # Сортировка
    sort_by = request.args.get('sort_by', 'id') # По умолчанию по ID
    sort_dir = request.args.get('sort_dir', 'ASC') # ASC или DESC
    
    # Защита от SQL-инъекций в сортировке (разрешаем только определенные поля)
    allowed_sort = ['title', 'author', 'pages', 'publisher', 'id']
    if sort_by not in allowed_sort:
        sort_by = 'id'
    if sort_dir.upper() not in ['ASC', 'DESC']:
        sort_dir = 'ASC'

    conn, cur = db_connect()
    
    # 2. Формирование SQL запроса
    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if title_filter:
        query += " AND title ILIKE %s"
        params.append(f"%{title_filter}%")
    
    if author_filter:
        query += " AND author ILIKE %s"
        params.append(f"%{author_filter}%")

    if publisher_filter:
        query += " AND publisher ILIKE %s"
        params.append(f"%{publisher_filter}%")

    if pages_min:
        query += " AND pages >= %s"
        params.append(pages_min)
        
    if pages_max:
        query += " AND pages <= %s"
        params.append(pages_max)

    # 3. Добавляем сортировку и пагинацию
    # Внимание: для ORDER BY нельзя использовать %s, вставляем f-строкой после проверки allowed_sort
    query += f" ORDER BY {sort_by} {sort_dir}"
    
    query += " LIMIT %s OFFSET %s"
    params.append(per_page)
    params.append(offset)

    # 4. Выполнение
    cur.execute(query, tuple(params))
    books = cur.fetchall()
    
    
    db_close(conn, cur)
    return jsonify(books)


@rgz.route('/rgz/api/books/', methods=['POST'])
def add_book():
    if session.get('login') != 'root':
        return abort(403)
    book = request.get_json()
    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO books (title, author, pages, publisher, cover_url)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """, (book['title'], book['author'], book['pages'], book['publisher'], book['cover_url']))
    new_id = cur.fetchone()['id']
    db_close(conn, cur)
    return {'id': new_id}, 201

@rgz.route('/rgz/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    if session.get('login') != 'root':
        return abort(403)
    
    conn, cur = db_connect()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    db_close(conn, cur)
    return '', 204

@rgz.route('/rgz/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    if session.get('login') != 'root':
        return abort(403)
    
    book = request.get_json()
    conn, cur = db_connect()
    cur.execute("""
        UPDATE books SET title=%s, author=%s, pages=%s, publisher=%s, cover_url=%s
        WHERE id=%s
    """, (book['title'], book['author'], book['pages'], book['publisher'], book['cover_url'], id))
    db_close(conn, cur)
    return jsonify(book)

@rgz.route('/rgz/api/books/<int:id>', methods=['GET'])
def get_book(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    db_close(conn, cur)
    if book is None:
        abort(404)
    return jsonify(book)
