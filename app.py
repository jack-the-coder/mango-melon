from os import environ
from re import sub
from codecs import encode
from sys import getsizeof

from werkzeug.routing import BuildError

from forms import SignUpForm, PostForm, SignInForm
from models import User, Post, DoesNotExist, DB

from werkzeug.exceptions import BadRequest
from flask import Flask, flash, redirect, url_for, render_template, g, abort, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import check_password_hash
from flask_admin import Admin
from flask_admin.conrib.peewee import ModelView


app = Flask(__name__)
app.secret_key = environ('skey0')


class AuthView(ModelView):
    column_exclude_list = ('avatar', 'password')
    form_excluded_columns = ['avatar']

    def is_accessible(self):
        if 'HEROKU' in environ:
            return current_user.is_authenticated and (g.user.username == environ['admin'])
        else:
            return current_user.is_authenticated

admin = Admin(app, name='PMM Admin')
admin.add_view(AuthView(User, 'User'))
admin.add_view(AuthView(Post, 'Post'))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in'


@login_manager.user_loader
def load_user(id):
    try:
        return User.get(User.id == id)
    except DoesNotExist:
        return None

@app.route('/')
def index(page=1):
    posts = None
    if current_user.is_authentiacted:
        posts = Post.select().paginate(page, 255)
    return render_template('index.html', posts=posts, page=page)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        flash('Welcome to Project Mango Melon! Please sign up. ')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/singin', methods=['GET', 'POST'])
@app.route('/singin/<action>', methods=['GET', 'POST'])
def sign_in(action=None):
    form = SignInForm()
    other_text = action
    if form.validate_on_submit():
        try:
            user = User.get(User.username ** form.name_email.data)
        except DoesNotExist:
            try:
                user = User.get(User.email ** form.name_email.data)
            except DoesNotExist:
                flash('The username or password is incorrect. ')
                return render_template('signin.html', form=form)
            else:
                user_exists = True
        else:
            user_exists = True

        if user_exists:
            if check_password_hash(user.password, form.password.data):
                if action:
                    try:
                        return redirect(url_for(action))
                    except BuildError:
                        # line 142 
