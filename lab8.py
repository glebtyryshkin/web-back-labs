from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html', login='anonymous')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', 
                             error='Имя пользователя не должно быть пустым')

    if not password_form:
        return render_template('lab8/register.html', 
                             error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                             error='Пользователь с таким логином уже существует!')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    
    return redirect('/lab8/') 

@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == '1'

    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember)  # remember=True сохраняет авторизацию после закрытия браузера 
        return redirect('/lab8/')

    return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    arts = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=arts)


from db.models import users, articles
from flask_login import login_required, current_user

@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = True if request.form.get('is_favorite') == '1' else False

    if not title:
        return render_template('lab8/create.html', error='Заголовок не должен быть пустым')
    if not article_text:
        return render_template('lab8/create.html', error='Текст статьи не должен быть пустым')

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        likes=0
    )

    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    art = articles.query.get_or_404(article_id)

    if art.login_id != current_user.id:
        return "Forbidden", 403

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=art)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title:
        return render_template('lab8/edit.html', article=art, error='Заголовок не должен быть пустым')
    if not article_text:
        return render_template('lab8/edit.html', article=art, error='Текст статьи не должен быть пустым')

    art.title = title
    art.article_text = article_text
    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    art = articles.query.get_or_404(article_id)

    if art.login_id != current_user.id:
        return "Forbidden", 403

    db.session.delete(art)
    db.session.commit()
    return redirect('/lab8/articles/')



@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')