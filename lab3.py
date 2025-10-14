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

@lab3.route('/lab3/clear_settings')

def clear_settings():

    resp = make_response(redirect('/lab3/settings'))
    
    resp.set_cookie('color', '', max_age=0)
    resp.set_cookie('bg_color', '', max_age=0)
    resp.set_cookie('font_size', '', max_age=0)
    resp.set_cookie('font_weight', '', max_age=0)
    
    return resp
    
PRODUCTS = [
    {"name": "Harley Benton EX-84 Modern EMG", "price": 60000, "brand": "Harley Benton", "type": "Эксплорер", "pickups": "EMG 81/60"},
    {"name": "Fender Player Stratocaster", "price": 85000, "brand": "Fender", "type": "Стратокастер", "pickups": "Single x3"},
    {"name": "Epiphone Les Paul Standard", "price": 55000, "brand": "Epiphone", "type": "Лес Пол", "pickups": "Humbucker x2"},
    {"name": "Ibanez RG421", "price": 48000, "brand": "Ibanez", "type": "Superstrat", "pickups": "Quantum"},
    {"name": "Squier Classic Vibe Strat", "price": 45000, "brand": "Squier", "type": "Стратокастер", "pickups": "Single x3"},
    {"name": "Jackson JS22 Dinky", "price": 38000, "brand": "Jackson", "type": "Superstrat", "pickups": "Humbucker x2"},
    {"name": "Yamaha Pacifica 112V", "price": 35000, "brand": "Yamaha", "type": "Стратокастер", "pickups": "HSS"},
    {"name": "ESP LTD EC-256", "price": 52000, "brand": "ESP", "type": "Лес Пол", "pickups": "Humbucker x2"},
    {"name": "Gibson Les Paul Studio", "price": 120000, "brand": "Gibson", "type": "Лес Пол", "pickups": "490R/498T"},
    {"name": "PRS SE Custom 24", "price": 75000, "brand": "PRS", "type": "PRS", "pickups": "Humbucker x2"},
    {"name": "Cort X100", "price": 28000, "brand": "Cort", "type": "Superstrat", "pickups": "Humbucker x2"},
    {"name": "Dean Vendetta XM", "price": 22000, "brand": "Dean", "type": "Superstrat", "pickups": "Humbucker x2"},
    {"name": "Schecter Omen Extreme", "price": 65000, "brand": "Schecter", "type": "Superstrat", "pickups": "Diamond Plus"},
    {"name": "Gretsch G2622 Streamliner", "price": 58000, "brand": "Gretsch", "type": "Полуакустика", "pickups": "Broad'Tron"},
    {"name": "Sterling by Music Man Cutlass", "price": 72000, "brand": "Sterling", "type": "Стратокастер", "pickups": "Single x3"},
    {"name": "Epiphone SG Standard", "price": 42000, "brand": "Epiphone", "type": "SG", "pickups": "Humbucker x2"},
    {"name": "Ibanez GRG121DX", "price": 32000, "brand": "Ibanez", "type": "Superstrat", "pickups": "Humbucker x2"},
    {"name": "Harley Benton SC-450", "price": 18000, "brand": "Harley Benton", "type": "Лес Пол", "pickups": "Humbucker x2"},
    {"name": "Fender American Professional Strat", "price": 150000, "brand": "Fender", "type": "Стратокастер", "pickups": "V-Mod Single"},
    {"name": "Gibson Explorer", "price": 140000, "brand": "Gibson", "type": "Эксплорер", "pickups": "Humbucker x2"}
]

@lab3.route('/lab3/products')

def products():
    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')
    
    min_price_form = request.args.get('min_price', '')
    max_price_form = request.args.get('max_price', '')
    
    min_price = min_price_form if min_price_form != '' else min_price_cookie
    max_price = max_price_form if max_price_form != '' else max_price_cookie
    
    if request.args.get('reset'):
        min_price = ''
        max_price = ''
    
    all_prices = [p['price'] for p in PRODUCTS]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)
    
    filtered_products = []
    if min_price or max_price:
        min_val = int(min_price) if min_price else 0
        max_val = int(max_price) if max_price else float('inf')
        
        if min_price and max_price and min_val > max_val:
            min_val, max_val = max_val, min_val
            min_price, max_price = max_price, min_price
        
        for product in PRODUCTS:
            price = product['price']
            if (not min_price or price >= min_val) and (not max_price or price <= max_val):
                filtered_products.append(product)
    else:
        filtered_products = PRODUCTS
    
    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price,
        max_price=max_price,
        min_all_price=min_all_price,
        max_all_price=max_all_price,
        count=len(filtered_products)
    ))
    
    if not request.args.get('reset'):
        if min_price:
            resp.set_cookie('min_price', min_price)
        if max_price:
            resp.set_cookie('max_price', max_price)
    else:
        resp.set_cookie('min_price', '', max_age=0)
        resp.set_cookie('max_price', '', max_age=0)
    
    return resp