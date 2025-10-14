import datetime

from flask import Blueprint, url_for, request, redirect, abort



lab1 = Blueprint('lab1', __name__)



@lab1.route('/lab1/')



def lab():
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

@lab1.route("/lab1/web")


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

@lab1.route("/lab1/author")


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

@lab1.route("/lab1/image")



def image():
    path = url_for("static", filename="/lab1/oak.jpg")
    style_path = url_for("static", filename="/lab1/lab1.css")
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

@lab1.route('/lab1/counter')


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

@lab1.route('/lab1/counter-cleaning')


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

@lab1.route("/lab1/info")


def info():
    return redirect("/lab1/author")

@lab1.route("/created")


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
