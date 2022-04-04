"""

"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.sql import extract
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User


@app.route("/")
def index():
    return render_template("index.html", title="main")

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/posts")
@login_required
def posts():
    return render_template("posts.html", title="posts")

@app.route("/profile", methods=['GET'])
@login_required
def profile():
    #profile = User.query.get_or_404(current_user(username)) #!!!!!!!!!?!!?!?!?!?!?!?!?!?!?!??!!?!?!?!?!?!
    profile = User.query.filter_by(username=current_user.username).first()
    month = profile.date.month
    year = profile.date.year
    return render_template("profile.html", title="profile", current_user=current_user, profile=profile, month=month, year=year)

@app.route("/news")
@login_required
def news():
    return render_template("news.html", title="news")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("register.html", title="register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        current_user.company = form.company.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
        form.website.data = current_user.website
        form.location.data = current_user.location
        form.company.data = current_user.company
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)