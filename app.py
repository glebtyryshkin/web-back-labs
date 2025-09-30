import datetime

from flask import Flask, url_for, request, redirect, abort, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            <menu>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </menu>
        </main>
        <footer>
            Тырышкин Глеб Алексеевич, ФБИ-31, 3 курс, 2025
        </footer>
    </body>
</html>
"""

@app.route("/lab1")


def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые 
            возможности.

        </main>
        <a href="/">На главную</a>
        <h2>Список роутов</h2>
        <li><a href="/lab1/web">WEB</a></li>
        <li><a href="/lab1/author">Автор</a></li>
        <li><a href="/lab1/image">Картинка</a></li>
        <li><a href="/lab1/counter">Счётчик</a></li>
        <li></lab1/counter-cleaning">Очистка счётчика</a></li>
        <li><a href="/lab1/info">Инфа</a></li>
        <li><a href="/created">Создали</a></li>
        <li><a href="/bad-request">400</a></li>
        <li><a href="/unauthorized">401</a></li>
        <li><a href="/payment-required">402</a></li>
        <li><a href="/forbidden">403</a></li>s
        <li><a href="/method-not-allowed">405</a></li>
        <li><a href="/teapot">418 Чайник</a></li>
        <li><a href="/cause-error">Делим на ноль</a></li>
    </body>
</html>
"""

@app.route("/lab1/web")

def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
           </body>
           <a href="/author">author</a>
        </html>""", 200, {
            "X-server": "sample",
            "Content-Type" : "text/plain; charset=utf-8"
            }

@app.route("/lab1/author")

def author():
    name = "Тырышкин Глеб Алексеевич"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")


def image():
    path = url_for("static", filename="oak.jpg")
    style_path = url_for("static", filename="lab1.css")
    return '''
<!doctype.html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
        <link rel="stylesheet" href="''' + style_path + '''">
    </body>
</html>''', 200, {
        "Content-Language": "ru",
        "X-Custom-Header": "CustomValue",
        "X-Another-Header": "AnotherValue",
        "Content-Type": "text/html; charset=utf-8"
    }

count = 0

@app.route('/lab1/counter')

def counter():
    global count 
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + ''' <br>
        Запрошенный адрес: ''' + str(url) + ''' <br>
        Ваш IP-адрес: ''' + str(client_ip) + ''' <br>
        <a href="/lab1/counter-cleaning">Очистить счётчик</a>
    </body>
</html>'''

@app.route('/lab1/counter-cleaning')

def counter_clean():
    global count 
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    count = 0

    return '''
<!doctype html>
<html>
    <body>
        Сброс счётчика.
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + ''' <br>
        Запрошенный адрес: ''' + str(url) + ''' <br>
        Ваш IP-адрес: ''' + str(client_ip) + ''' <br>
        <a href="/lab1/counter">Вернуться назад</a>
    </body>
</html>'''

@app.route("/lab1/info")

def info():
    return redirect("/lab1/author")


@app.route("/created")

def created():
    return '''
<! doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано ...</i></div>
    </body>
</html>
''', 201

# app = Flask(__name__)

logs = []

@app.errorhandler(404)


def not_found(err):
    global logs
    path = url_for("static", filename="2725947.jpg")
    style_path = url_for("static", filename="lab1.css")
    time = str(datetime.datetime.now())
    client_ip = request.remote_addr
    url = request.url
    log_entry = f"{time}, пользователь {client_ip} зашел на адрес {url}"
    logs.append(log_entry)
    log_display = "\n".join(logs)
    return '''
<!doctype.html>
<html>
    <body>
        <h1>Упс... Хьюстон, у нас проблемы</h1>
        <img src="''' + path + '''">
        <link rel="stylesheet" href="''' + style_path + '''">
        <h2>Ваш IP-адрес: ''' + client_ip + '''</h2>
        <h2>Дата доступа: ''' + time + '''</h2>
        <a href="/">На главную</a>
        <h2>Лог:</h2>
        <pre>''' + log_display + '''</pre>
    </body>
</html>''', 404

@app.route('/bad-request')

def bad_request():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за некорректного синтаксиса.</p>
    </body>
</html>
''', 400

@app.route('/unauthorized')

def unauthorized():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Для доступа к ресурсу требуется аутентификация.</p>
    </body>
</html>
''', 401

@app.route('/payment-required')

def payment_required():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402 Payment Required</h1>
        <p>Зарезервировано для будущего использования.</p>
    </body>
</html>
''', 402

@app.route('/forbidden')

def forbidden():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403 Forbidden</h1>
        <p>Сервер понял запрос, но отказывается его авторизовать.</p>
    </body>
</html>
''', 403

@app.route('/method-not-allowed')

def method_not_allowed():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Используемый метод запроса не поддерживается данным ресурсом.</p>
    </body>
</html>
''', 405

@app.route('/teapot')

def teapot():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я - чайник. Не могу заваривать кофе.</p>
    </body>
</html>
''', 418

@app.route("/cause-error")

def caurse_error():
    return 1/0

@app.errorhandler(500)

def internal_error(error):
    return """
<!doctype html>
<html>
    <body>
        <h1>Ой-ой, 500 - внутренняя ошибка сервера.<h1>
        <p>Что-то пошло не так... Попробуйте вернуться на <a
            href="/">главную</a>.</p>
    </body>
</html>
""", 500

@app.route('/lab2/a/')
def a():
    return 'ok'

@app.route('/lab2/a')
def a_mod():
    return 'not ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Цветок № {flower_id + 1}</h1>
            <p>Название: {flower_list[flower_id]}</p>
            <a href="/lab2/all_flowers/">Смотреть все цветы</a>
        </body>
    </html>
    '''
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка:  {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def add_flower_no_name():
    abort(400, 'вы не задали имя цветка')

@app.route('/lab2/all_flowers/')
def all_flowers():
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Все цветы</h1>
            <p>Количество цветов: {len(flower_list)}</p>
            <ul>
                {"".join(f"<li>{flower}</li>" for flower in flower_list)}
            </ul>
            <a href="/lab2/clear_flowers/">Очистить список</a>
        </body>
    </html>
    '''

@app.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers/')

@app.route('/lab2/example')
def example():
    name = 'Глеб Тырышкин'
    lab_num = 2
    group_num = 'ФБИ-31'
    course_num = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'aneльcины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'Maнгo', 'price': 321}
    ]
    return render_template('example.html', 
                           name=name, group_num=group_num, 
                           course_num=course_num, lab_num=lab_num, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/books')
def books_route():
    books = [
        {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225},
        {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
        {'author': 'Джейн Остин', 'title': 'Гордость и предубеждение', 'genre': 'Роман', 'pages': 432},
        {'author': 'Джордж Орвелл', 'title': '1984', 'genre': 'Дистопия', 'pages': 328},
        {'author': 'Габриэль Гарсия Маркес', 'title': 'Сто лет одиночества', 'genre': 'Магический реализм', 'pages': 417},
        {'author': 'Фрэнсис Скотт Фицджеральд', 'title': 'Великий Гэтсби', 'genre': 'Роман', 'pages': 180},
        {'author': 'Дж.Р.Р. Толкин', 'title': 'Властелин колец', 'genre': 'Фэнтези', 'pages': 1178},
        {'author': 'Маргарет Митчелл', 'title': 'Унесённые ветром', 'genre': 'Роман', 'pages': 1037},
        {'author': 'Харпер Ли', 'title': 'Убить пересмешника', 'genre': 'Роман', 'pages': 281},
        {'author': 'Джон Стейнбек', 'title': 'Гроздья гнева', 'genre': 'Роман', 'pages': 464}
    ]
    return render_template('books.html', books=books)

@app.route('/lab2/animals')
def berries_route():
    animals = [
        {'name': 'Повар', 'description': 'Хомякович, любит готовить.', 'image': 'animal_1.jpg'},
        {'name': 'Красавчик', 'description': 'Вайбик имеется.', 'image': 'animal_2.jpg'},
        {'name': 'Скромный диджей', 'description': 'Начинающий диджей, не судите строго', 'image': 'animal_3.jpg'},
        {'name': 'Огородник', 'description': 'Маленький чихуа-хуа любит собирать урожай', 'image': 'animal_4.jpg'},
        {'name': 'Бобик', 'description': 'Устал и любит сидеть. Просто сидеть.', 'image': 'animal_5.jpg'},
        {'name': 'Овечка-айтишник', 'description': 'Програет и распутывает самые запутанные истории.', 'image': 'animal_6.jpg'},
        {'name': 'Васёк', 'description': 'Рубится в свой старый комп после работы', 'image': 'animal_7.jpg'},
        {'name': 'Кайфарики', 'description': 'Заходят как-то в бар два котёнка...', 'image': 'animal_8.jpg'},
        {'name': 'Скейтеры', 'description': 'Безбашенные ребята', 'image': 'animal_9.jpg'},
        {'name': 'Пилот', 'description': 'Летает на Миг-29. Гроза поросят', 'image': 'animal_10.jpg'},
        {'name': 'Рыбак', 'description': 'Настраивается на крупный улов', 'image': 'animal_11.jpg'},
        {'name': 'Подкастер', 'description': 'Идёт медведь по дороге, видит машина горит, сел в неё и сгорел', 'image': 'animal_12.jpg'},
        {'name': 'Игрок в покер', 'description': 'Азарт - моё второе имя (первое - мяу).', 'image': 'animal_13.jpg'},
        {'name': 'Профессиональный диджей', 'description': 'Устраивает рейвы мирового масштаба', 'image': 'animal_14.jpg'},
        {'name': 'Офис', 'description': 'Ало, подростки? Дада СВАГА!', 'image': 'animal_15.jpg'},
        {'name': 'Адьос-амигос', 'description': 'Покатился куда подальше', 'image': 'animal_16.jpg'},
        {'name': 'Трюкачи', 'description': 'Фристайло, ракамакафо', 'image': 'animal_17.jpg'},
        {'name': 'Невезучий', 'description': 'АААААааааааааа, ветер!', 'image': 'animal_18.jpg'},
        {'name': 'Гитарист', 'description': 'Какова музыка на вкус?', 'image': 'animal_19.jpg'},
        {'name': 'Рокер', 'description': 'Дайте людям рому!', 'image': 'animal_20.jpg'},
        {'name': 'Эстет', 'description': 'Ловит красивые вайбы и ценит каждый момент.', 'image': 'animal_21.jpg'},
    ]
    return render_template('animals.html', animals=animals)