from flask import Flask, render_template
from werkzeug.utils import redirect

from data import db_session
from data.user import RegisterForm
from data.users import User
from data.LoginForm import LoginForm
from data.CommentForm import CommentForm
from flask_login import login_user, LoginManager, login_required, logout_user
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

user = None


names = []


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first()\
                or db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            global names
            conn = sqlite3.connect('db/users.db')
            cursor = conn.cursor()
            names = cursor.execute("""SELECT name FROM users""").fetchall()
            conn.commit()
            conn.close()
            return redirect("/main")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def index():
    return render_template('information.html')


@app.route('/pony_run')
def pony_run():
    global names
    comments = []
    all_stars = []
    stars_count = []
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()
    comments1 = cursor.execute("""SELECT comments_pony_run FROM users""").fetchall()
    stars = cursor.execute("""SELECT stars_pony_run FROM users""").fetchall()
    for i in stars:
        all_stars.append(*i)
    for i in stars:
        if i != (None,):
            stars_count.append(*i)
    for i in comments1:
        comments.append([*names[comments1.index(i)], *i])
    if len(comments) > 10:
        comments = comments[len(comments) - 10:]
    conn.commit()
    conn.close()
    if len(stars_count) != 0:
        star = sum(stars_count) / len(stars_count)
        star = round(star, 1)
    else:
        star = '-'
    return render_template('pony_run.html', comments=comments, stars=star, star_list=all_stars)


@app.route('/politopy')
def politopy():
    global names
    comments = []
    all_stars = []
    stars_count = []
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()
    comments1 = cursor.execute("""SELECT comments_politopy FROM users""").fetchall()
    stars = cursor.execute("""SELECT stars_politopy FROM users""").fetchall()
    for i in stars:
        all_stars.append(*i)
    for i in stars:
        if i != (None,):
            stars_count.append(*i)
    for i in comments1:
        comments.append([*names[comments1.index(i)], *i])
    if len(comments) > 10:
        comments = comments[len(comments) - 10:]
    conn.commit()
    conn.close()
    if len(stars_count) != 0:
        star = sum(stars_count) / len(stars_count)
        star = round(star, 1)
    else:
        star = '-'
    return render_template('politopy.html', comments=comments, stars=star, star_list=all_stars)


@app.route('/profile')
def profile():
    return render_template('profile.html', name=user.name, email=user.email, about=user.about,
                           comments_politopy=user.comments_politopy, comments_pony_run=user.comments_pony_run,
                           politopy_star=user.stars_politopy, pony_run_star=user.stars_pony_run)


@app.route('/main')
def main_page():
    return render_template('first.html')


@app.route('/comments_politopy', methods=['GET', 'POST'])
def comment_page_politopy():
    global user
    form = CommentForm()
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()
    sql_select_query_1 = """UPDATE users SET comments_politopy = ? WHERE email = ?"""
    sql_select_query_2 = """UPDATE users SET stars_politopy = ? WHERE email = ?"""
    cursor.execute(sql_select_query_1, (form.comments.data, user.email,))
    cursor.execute(sql_select_query_2, (form.stars.data, user.email,))
    conn.commit()
    conn.close()
    return render_template('comments.html', form=form)


@app.route('/comments_pony_run', methods=['GET', 'POST'])
def comments_pony_run():
    global user
    form = CommentForm()
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()
    sql_select_query_1 = """UPDATE users SET comments_pony_run = ? WHERE email = ?"""
    sql_select_query_2 = """UPDATE users SET stars_pony_run = ? WHERE email = ?"""
    cursor.execute(sql_select_query_1, (form.comments.data, user.email,))
    cursor.execute(sql_select_query_2, (form.stars.data, user.email,))
    conn.commit()
    conn.close()
    return render_template('comments.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/users.db')

    app.run()


if __name__ == '__main__':
    main()
