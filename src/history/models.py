# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'
from containers import db
from sqlalchemy import func


class TimeTrackedMixin(object):
    date_created = db.Column(db.DateTime, default=func.now())
    date_updated = db.Column(db.DateTime, onupdate=func.now())

    @staticmethod
    def format_date(date):
        """
        Override this for custom formatting
        :param date:
        :return:
        """
        return date.strftime('%d-%m-%Y %H:%M:%S')

    @property
    def date_created_display(self):
        return self.format_date(self.date_created)

    @property
    def date_updated_display(self):
        return self.format_date(self.date_updated)
