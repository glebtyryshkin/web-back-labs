import datetime

from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response





lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')


def lab():
    name = request.cookies.get('name', 'Незнакомец')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'неизвестно')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')

def coockie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/cookie/delete')

def delete_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')

def form1():
    errors = {}
    user = request.args.get('user')

    if user == '':
        errors['user'] = 'Заполните поле!'
    
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html',user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')

def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    elif drink == 'green-tea':
        price = 70


    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on': 
        price += 10
        
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')

def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')

def settings():
    text_color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_weight = request.args.get('font_weight')

    if any([text_color, bg_color, font_size, font_weight]):
        resp = make_response(redirect('/lab3/settings'))
        if text_color:
            resp.set_cookie('color', text_color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            if font_size.isdigit():
                resp.set_cookie('font_size', font_size + 'px')
            else:
                resp.set_cookie('font_size', font_size)
        if font_weight:
            resp.set_cookie('font_weight', font_weight)
        return resp

    color = request.cookies.get('color')
    bg = request.cookies.get('bg_color')
    size = request.cookies.get('font_size')
    weight = request.cookies.get('font_weight')

    return render_template('lab3/settings.html',
                           color=color, bg_color=bg,
                           font_size=size, font_weight=weight)

@lab3.route('/lab3/ticket')

def ticket():
    errors = {}
    return render_template('lab3/ticket.html', errors=errors)

@lab3.route('/lab3/ticket_result')

def ticket_result():


    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    errors = {}
    if not fio:
        errors['fio'] = "Заполните поле"
    if not shelf:
        errors['shelf'] = "Выберите полку"
    if not age:
        errors['age'] = "Заполните поле"
    elif not age.isdigit() or int(age) < 1 or int(age) > 120:
        errors['age'] = "Возраст должен быть от 1 до 120 лет"
    if not departure:
        errors['departure'] = "Заполните поле"
    if not destination:
        errors['destination'] = "Заполните поле"
    if not date:
        errors['date'] = "Выберите дату"
    
    if errors:
        return render_template('lab3/ticket.html', 
                             errors=errors,
                             fio=fio or '',
                             age=age or '',
                             departure=departure or '',
                             destination=destination or '',
                             date=date or '')
    

    price = 700 if int(age) < 18 else 1000
    
    if shelf in ['lower', 'side_lower']:
        price += 100
    if linen == 'on':
        price += 75
    if luggage == 'on':
        price += 250
    if insurance == 'on':
        price += 150
    
    ticket_type = "Детский билет" if int(age) < 18 else "Взрослый билет"
    
    return render_template('lab3/ticket_result.html',
                         fio=fio,
                         shelf=shelf,
                         linen=linen,
                         luggage=luggage,
                         age=age,
                         departure=departure,
                         destination=destination,
                         date=date,
                         insurance=insurance,
                         price=price,
                         ticket_type=ticket_type)
