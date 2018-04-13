#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A Study for Flask and Flask-Login.

    by Kei Onimaru <otegami@devel.keys.jp>
"""

from flask import Flask
from flask import render_template, request, redirect, \
flash, url_for
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, \
current_user

from mogmog.userlist import LoginUser, UserList
from mogmog.views import LoginForm, LogoutConfirmForm


app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

user_list = UserList('sqlite:///userlist.sqlite3')

@app.route('/')
def path_route():
    return render_template('index.html')

@app.route('/sample')
@login_required
def path_sample():
    return render_template('sample.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        flash('You (user: {}) are still logged in.'.format(current_user.username))
        return redirect(url_for('path_sample'))
    else:
        form = LoginForm()
        if request.method == 'GET':
            return render_template('login.html', form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                username = request.form.get('username')
                password = request.form.get('password')
                if user_list.authenticate_user(username, password):
                # if username == password:
                    login_user(LoginUser(username))
                    flash('Login successfully.', 'info')
                    return redirect(request.args.get('next') or url_for('path_route'))
                else:
                    flash('Invalid user name or password.', 'error')
                    return redirect(url_for('user_login'))
        flash('Invalid operation.', 'error')
        return redirect(url_for('user_login'))

@app.route('/logout', methods=['GET', 'POST'])
def user_logout():
    if not current_user.is_authenticated:
        flash('You are not logged in or still logged out.')
        return redirect(url_for('path_route'))
    else:
        form = LogoutConfirmForm()
        if request.method == 'GET':
            return render_template('logout_confirm.html', form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                if request.form.get('confirm'):
                    logout_user()
                    flash('Logged out.', 'info')
                    return redirect(url_for('user_login'))
        flash('Invalid operation.', 'error')
        return redirect(url_for('user_login'))

@login_manager.user_loader
def load_user(username):
    return LoginUser(username)
