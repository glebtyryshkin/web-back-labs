from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')

def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')

def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])

def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!!')
    if x2 == '0':
            return render_template('lab4/div.html', error='Делить на 0 нельзя!!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')

def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])

def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = 0 if x1 == '' else int(x1)
    x2 = 0 if x2 == '' else int(x2)
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')

def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])

def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = 1 if x1 == '' else int(x1)
    x2 = 1 if x2 == '' else int(x2)
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')

def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])

def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')

def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])

def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть нулями!!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])

def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')
    max_trees = 10 

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1

    elif operation == 'plant':
        if tree_count < max_trees:
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    {'login': 'root', 'password': 'root', 'name': 'Администратор', 'gender': 'male'},
    {'login': 'gleb', 'password': '111', 'name': 'Глеб Тырышкин', 'gender': 'male'},
    {'login': 'anna', 'password': '777', 'name': 'Анна Сидорова', 'gender': 'female'},
]

def get_current_user():
    if 'login' in session:
        for user in users:
            if user['login'] == session['login']:
                return user
    return None

@lab4.route('/lab4/register', methods=['GET', 'POST'])

def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    gender = request.form.get('gender')
    
    errors = []
    
    if not login:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    if not password_confirm:
        errors.append('Не введено подтверждение пароля')
    if not name:
        errors.append('Не введено имя')
    
    if password != password_confirm:
        errors.append('Пароли не совпадают')
    
    for user in users:
        if user['login'] == login:
            errors.append('Пользователь с таким логином уже существует')
            break
    
    if errors:
        return render_template('lab4/register.html', 
                             errors=errors,
                             login=login,
                             name=name,
                             gender=gender)
    
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)
    
    session['login'] = login
    return redirect('/lab4/login')

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user = get_current_user()
    return render_template('lab4/users.html', 
                         users=users, 
                         current_user=current_user)

@lab4.route('/lab4/users/delete_self', methods=['POST'])

def delete_self():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_login = session['login']

    global users
    users = [user for user in users if user['login'] != current_login]
    
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users/edit_self', methods=['GET', 'POST'])
def edit_self():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user = get_current_user()
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', 
                             user=current_user)
    
    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    gender = request.form.get('gender')
    
    errors = []
    
    if not login:
        errors.append('Не введён логин')
    if not name:
        errors.append('Не введено имя')
    
    for user in users:
        if user['login'] == login and user['login'] != current_user['login']:
            errors.append('Пользователь с таким логином уже существует')
            break
    
    if password and password != password_confirm:
        errors.append('Пароли не совпадают')
    
    if errors:
        return render_template('lab4/edit_user.html', 
                             user=current_user,
                             errors=errors,
                             login=login,
                             name=name,
                             gender=gender)
    
    for user in users:
        if user['login'] == current_user['login']:
            user['login'] = login
            user['name'] = name
            user['gender'] = gender

            if password:
                user['password'] = password
            break
    
    session['login'] = login
    
    return redirect('/lab4/users')


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_name = ''
            for user in users:
                if user['login'] == session['login']:
                    user_name = user['name']
                    break
            return render_template('lab4/login.html', authorized=authorized, 
                                                        user_name=user_name)
        else:
            return render_template('lab4/login.html', authorized=False)

    login = request.form.get('login')
    password = request.form.get('password')
    
    errors = []
    if not login:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    
    if errors:
        return render_template('lab4/login.html', 
                             authorized=False, 
                             login=login, 
                             errors=errors)

    for user in users:
        if user['login'] == login and user['password'] == password:
            session['login'] = login
            return redirect('/lab4/login')

    return render_template('lab4/login.html', 
                         authorized=False, 
                         login=login, 
                         errors=['Неверные логин или пароль'])

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ''
    snowflakes = 0
    temperature = None
    
    if request.method == 'POST':
        temp_str = request.form.get('temperature')
        
        if not temp_str:
            message = 'Ошибка: не задана температура'
        else:
            try:
                temperature = float(temp_str)
                
                if temperature < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif temperature > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temperature <= -9:
                    message = f'Установлена температура: {temperature}°C'
                    snowflakes = 3
                elif -8 <= temperature <= -5:
                    message = f'Установлена температура: {temperature}°C'
                    snowflakes = 2
                elif -4 <= temperature <= -1:
                    message = f'Установлена температура: {temperature}°C'
                    snowflakes = 1
                    
            except ValueError:
                message = 'Ошибка: введите числовое значение температуры'
    
    return render_template('lab4/fridge.html', 
                         message=message, 
                         snowflakes=snowflakes, 
                         temperature=temperature)

@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])

def grain_order():
    grain_types = {
        'barley': {'name': 'ячмень', 'price': 12000},
        'oats': {'name': 'овёс', 'price': 8500},
        'wheat': {'name': 'пшеница', 'price': 9000},
        'rye': {'name': 'рожь', 'price': 15000}
    }
    
    message = ''
    order_details = {}
    error = ''
    
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight_str = request.form.get('weight')
        
        if not grain_type:
            error = 'Выберите тип зерна'
        elif not weight_str:
            error = 'Не указан вес'
        else:
            try:
                weight = float(weight_str)
                if weight <= 0:
                    error = 'Вес должен быть положительным числом'
                elif weight > 100:
                    error = 'Такого объёма сейчас нет в наличии'
                else:

                    grain_info = grain_types[grain_type]
                    base_price = grain_info['price']
                    total = base_price * weight
                    
                    discount = 0
                    if weight > 10:
                        discount = total * 0.1
                        total -= discount
                    
                    order_details = {
                        'grain_name': grain_info['name'],
                        'weight': weight,
                        'total': total,
                        'discount': discount,
                        'has_discount': discount > 0
                    }
                    
            except ValueError:
                error = 'Введите корректное числовое значение веса'
    
    return render_template('lab4/grain_order.html', 
                         grain_types=grain_types,
                         order_details=order_details,
                         error=error)
