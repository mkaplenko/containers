# -*- coding: utf-8 -*-
__author__ = 'mkaplenko'

from flask_wtf import Form
import wtforms
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from containers.models import Manufacturer, Investor, Container, Renter, RentPeriod
from containers.widgets import DatePicker


class RenterForm(Form):
    name = wtforms.StringField(u'Название', validators=[DataRequired()])
    inn = wtforms.StringField(u'ИНН')
    ogrn = wtforms.StringField(u'ОГРН')
    phone_contacts = wtforms.TextAreaField(u'Телефоны и контактные лица')
    email = wtforms.StringField(u'E-Mail', validators=[Email()])
    comment = wtforms.TextAreaField(u'Примечание')


class ManufacturerForm(Form):
    name = wtforms.StringField(u'Наименование', validators=[DataRequired()])


class InvestorForm(Form):
    name = wtforms.StringField(u'Название', validators=[DataRequired()])
    phone = wtforms.StringField(u'Телефонный номер')
    manager = wtforms.StringField(u'Менеджер')
    comment = wtforms.TextAreaField(u'Комметарий')


class ContainerForm(Form):
    TYPES = (
        ('sea', u'Морской'),
        ('earth', u'Блок контейнер')
    )

    number = wtforms.IntegerField(u'Порядковый номер', validators=[DataRequired()])
    invent_number = wtforms.StringField(u'Инвентарный номер', validators=[DataRequired()])
    manufacturer = QuerySelectField(u'Производитель', query_factory=lambda: Manufacturer.query.all())
    investor = QuerySelectField(u'Инвестор', query_factory=lambda: Investor.query.all())
    buy_cost = wtforms.DecimalField(u'Закупочная цена', validators=[DataRequired()])
    container_type = wtforms.SelectField(u'Тип', validators=[DataRequired()], choices=TYPES)
    status = wtforms.SelectField(u'Статус', validators=[DataRequired()], choices=Container.STATUSES)


class RentContainerPeriodForm(Form):
    STATUSES = (
        ('closed', u'Закончена'),
        ('open', u'Текущая аренда')
    )

    begin_date = wtforms.DateField(u'Дата начала аренды', validators=[DataRequired()], widget=DatePicker())
    renter = QuerySelectField(u'Арендатор', query_factory=lambda: Renter.query.all())
    summ = wtforms.DecimalField(u'Сумма оплаты', validators=[DataRequired()])
    address = wtforms.TextAreaField(u'Адрес установки', validators=[DataRequired()])
    total = wtforms.DecimalField(u'Стоимость доставки + вывоза', validators=[DataRequired()])

    status = wtforms.SelectField(u'Статус аренды', validators=[DataRequired()], choices=STATUSES, default='open')


class RentPeriodItemForm(Form):
    PAYMENT_STATUSES = (
        ('wait', u'Ожидает оплаты'),
        ('payed', u'Оплачен')
    )
    begin_date = wtforms.DateField(u'Дата начала месяца', validators=[DataRequired()], widget=DatePicker())
    end_date = wtforms.DateField(u'Дата окончания месяца', validators=[DataRequired()], widget=DatePicker())
    summ = wtforms.DecimalField(u'Сумма оплаты за месяц', validators=[DataRequired()])
    period_payment_status = wtforms.SelectField(u'Статус оплаты', validators=[DataRequired()], choices=PAYMENT_STATUSES,
                                                default='wait')