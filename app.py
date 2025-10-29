import datetime

from flask import Flask, url_for, request, redirect, abort, render_template

from lab1 import lab1

from lab2 import lab2

from lab3 import lab3

from lab4 import lab4

from lab5 import lab5


app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

@app.route('/')
@app.route('/index')


def index():
    return render_template('/lab2/index.html')

logs = []

@app.errorhandler(404)



def not_found(err):
    global logs
    path = url_for('static', filename='/lab1/2725947.jpg')
    style_path = url_for('static', filename='/lab1/lab1.css')
    time = str(datetime.datetime.now())
    client_ip = request.remote_addr
    url = request.url
    log_entry = f"{time}, пользователь {client_ip} зашел на адрес {url}"
    logs.append(log_entry)
    log_display = '\n'.join(logs)
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
