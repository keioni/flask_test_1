#!/usr/bin/env python
#! coding: utf-8

from flask import Flask
from flask import render_template, request, redirect, session, abort, \
make_response, flash, url_for
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user

import user

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def path_route():
    return render_template('index.html')

@app.route('/sample')
@login_required
def path_sample():
    if not session.get('sid'):
        flash('Login required to show this page.', category='warn')
        return redirect(url_for('user_login'))
    else:
        return render_template('sample.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if session.get('sid'):
        return redirect(url_for('path_sample'))
    else:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if user.authenticate(username, password):
                session['sid'] = username
                return redirect(url_for('path_sample'))
            else:
                flash('Invalid user name or password.', category='error')
                return redirect(url_for('user_login'))

@app.route('/logout', methods=['GET', 'POST'])
def user_logout():
    user = session.get('sid')
    if user:
        if request.method == 'GET':
            return render_template('logout_confirm.html')
        elif request.method == 'POST':
            confirmed = request.form.get('confirm')
            if confirmed:
                session.pop('sid', None)
                flash('Logout successfully.', category='info')
                return redirect(url_for('user_login'))
            else:
                return redirect(url_for('path_sample'))
    else:
        return render_template('not_logged_in.html')

@login_manager.user_loader
def load_user(username):
    return user.User.get_id(username)