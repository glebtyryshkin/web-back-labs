import datetime

from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response





lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')


def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

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
