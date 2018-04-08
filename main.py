#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, request, redirect, session, abort, \
make_response, flash, url_for
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, \
current_user

import user
from user import User

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

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
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if user.authenticate(username, password):
                u = User(username)
                login_user(u)
                return redirect(request.args.get("next"))
            else:
                flash('Invalid user name or password.', 'error')
                return redirect(url_for('user_login'))

@app.route('/logout', methods=['GET', 'POST'])
def user_logout():
    if not current_user.is_authenticated:
        flash('You are not logged in or still logged out.')
        return redirect(url_for('path_route'))
    else:
        if request.method == 'GET':
            return render_template('logout_confirm.html')
        elif request.method == 'POST':
            if request.form.get('confirm'):
                logout_user()
                flash('Logout successfully.', 'info')
                return redirect(url_for('user_login'))
            else:
                # unreachable
                return redirect(url_for('path_sample'))

@login_manager.user_loader
def load_user(username):
    return User(username)