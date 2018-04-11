# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    # username = StringField('username', validators=[InputRequired()])
    # password = PasswordField('password', validators=[InputRequired()])
    # username = StringField('username', validators=[DataRequired()])
    # password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')
