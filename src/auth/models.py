# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'

from containers import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.ext.login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, email, password, is_admin=False, first_name=None, last_name=None):
        user = cls()
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = is_admin
        user.password = password

        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))