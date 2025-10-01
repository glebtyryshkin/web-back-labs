import datetime

from flask import Blueprint, url_for, request, redirect, abort, render_template



lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')

def a():
    return 'ok'

@lab2.route('/lab2/a')

def a_mod():
    return 'not ok'

flower_list = [
    {'name': 'роза', 'price': 100},
    {'name': 'тюльпан', 'price': 50},
    {'name': 'незабудка', 'price': 30},
    {'name': 'ромашка', 'price': 20}
]

@lab2.route('/lab2/flowers/<int:flower_id>')

def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower.html', flower=flower, id=flower_id)

@lab2.route('/lab2/add_flower/', methods=['POST'])

def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')
    if not name or not price:
        abort(400, 'Не заданы имя или цена')
    try:
        price = int(price)
    except ValueError:
        abort(400, 'Цена должна быть числом')
    flower_list.append({'name': name, 'price': price})
    return redirect('/lab2/all_flowers/')

@lab2.route('/lab2/all_flowers/')

def all_flowers():
    return render_template('all_flowers.html', flowers=flower_list)

@lab2.route('/lab2/delete_flower/<int:flower_id>')

def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    del flower_list[flower_id]
    return redirect('/lab2/all_flowers/')

@lab2.route('/lab2/clear_flowers/')

def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers/')

@lab2.route('/lab2/add_flower/')

def add_flower_no_name():
    abort(400, 'вы не задали имя цветка')

@lab2.route('/lab2/example')

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

@lab2.route('/lab2/')

def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')

def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')

def calc(a, b):
    return render_template('calc.html', a=a, b=b)

@lab2.route('/lab2/calc/')

def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')

def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/books')

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

@lab2.route('/lab2/animals')
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