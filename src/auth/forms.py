# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField(u'Пароль', validators=[DataRequired()])
    remember_me = BooleanField(u'Запонить меня')
