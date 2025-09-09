from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/index")
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
</html>'''

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

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404