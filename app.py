import datetime

from flask import Flask, url_for, request, redirect, abort

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

flower_list = ('роза', 'тюльпан', 'незабудка', 'ромашка')

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if 0 < flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]