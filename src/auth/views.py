# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'
from flask import render_template
from auth import bp


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')