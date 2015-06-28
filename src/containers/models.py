# coding: utf-8
from containers import db
from sqlalchemy import func
from history.models import TimeTrackedMixin


class Renter(TimeTrackedMixin, db.Model):
    __tablename__ = 'renters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    inn = db.Column(db.String())
    ogrn = db.Column(db.String())
    phone_contacts = db.Column(db.String())
    email = db.Column(db.String())
    comment = db.Column(db.String())

    periods_query = db.relationship('RentPeriod', uselist=True, lazy='dynamic')

    def __unicode__(self):
        return self.name


class Manufacturer(TimeTrackedMixin, db.Model):
    __tablename__ = 'manufacturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __unicode__(self):
        return self.name


class Investor(TimeTrackedMixin, db.Model):
    __tablename__ = 'investors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    manager = db.Column(db.String)
    comment = db.Column(db.String)

    def __unicode__(self):
        return self.name


class Container(TimeTrackedMixin, db.Model):
    __tablename__ = 'containers'

    STATUSES = (
        ('sklad', u'На складе'),
        ('sale', u'Продан'),
        ('arend', u'В аренде'),
        ('reserved', u'Зарезервирован'),
        ('remont', u'Требует ремонта'),
        ('for go', u'Заявлен к вывозу')
    )

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    invent_number = db.Column(db.String(30), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    manufacturer_id = db.Column(db.ForeignKey('manufacturers.id'), nullable=False)
    investor_id = db.Column(db.ForeignKey('investors.id'), nullable=True)
    buy_cost = db.Column(db.Numeric(10, 2), nullable=False)
    container_type = db.Column(db.Enum(*('sea', 'earth'), name='container_types'), default='earth', nullable=False)
    status = db.Column(db.Enum(*[x[0] for x in STATUSES], name='container_statuses'), default='earth', nullable=False)
    photo = db.Column(db.String, nullable=True)

    manufacturer = db.relationship(Manufacturer, backref='containers')
    investor = db.relationship(Investor, backref='containers')

    periods_query = db.relationship('RentPeriod', lazy='dynamic', uselist=True)

    @property
    def status_verbose(self):
        for k, v in self.STATUSES:
            if k == self.status:
                return v
        return None

    @property
    def container_type_verbose(self):
        if self.container_type == 'sea':
            return u'Морской'
        elif self.container_type == 'earth':
            return u'Контейнер'
        else:
            return None

    @property
    def current_rent_period(self):
        return self.periods_query.filter(RentPeriod.status == 'open').order_by(RentPeriod.date_created).first()


class RentPeriod(TimeTrackedMixin, db.Model):
    __tablename__ = 'rent_periods'

    id = db.Column(db.Integer, primary_key=True)
    begin_date = db.Column(db.Date(), nullable=False)
    renter_id = db.Column(db.ForeignKey('renters.id'), nullable=False)
    container_id = db.Column(db.ForeignKey('containers.id'), nullable=False)
    summ = db.Column(db.Numeric(10, 2), nullable=False)
    address = db.Column(db.String(), nullable=False)
    total = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Enum(*('open', 'closed'), name='period_statuses'), default='open', nullable=False)

    renter = db.relationship(Renter, lazy='joined', uselist=False)
    container = db.relationship(Container, lazy='joined', uselist=False)


class RentPeriodItem(TimeTrackedMixin, db.Model):
    __tablename__ = 'rentperiod'

    PAYMENT_STATUSES = (
        ('wait', u'Ожидает оплаты'),
        ('payed', u'Оплачен')
    )

    id = db.Column(db.Integer, primary_key=True)
    rent_period_id = db.Column(db.ForeignKey('rent_periods.id'), nullable=False)
    begin_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    summ = db.Column(db.Numeric(10, 2), nullable=False)
    period_payment_status = db.Column(db.Enum(*[x[0] for x in PAYMENT_STATUSES],
                                              name='rent_period_payment_statuses'), default='wait', nullable=False)

    rent_period = db.relationship(RentPeriod, lazy='joined', uselist=False,
                                  backref=db.backref('period_items', uselist=True, lazy='joined'))