# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'

from flask import Blueprint


bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static', url_prefix='/auth')
