# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'
from flask import render_template, redirect, url_for, request, flash
from auth import bp
from auth.forms import LoginForm
from auth.models import User
from flask.ext.login import login_user


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash(u'Неверный e-mail или пароль', 'danger')
    for field, errors in form.errors.iteritems():
        for error in errors:
            flash(u'Ошибка в поле {}. {}'.format(field, error), 'danger')
    return render_template('auth/login.html', form=form)