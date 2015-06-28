# coding: utf-8
import datetime

from flask import render_template, redirect, url_for, current_app, flash, request, abort
from flask.ext.login import login_required
from containers import app, db
from containers.models import Container, Manufacturer, Investor, Renter, RentPeriod, RentPeriodItem
from containers.forms import ContainerForm, ManufacturerForm, InvestorForm, RenterForm, RentContainerPeriodForm, RentPeriodItemForm


@app.route('/')
def index():
    return redirect(url_for('containers'))


@app.route('/periods/')
@login_required
def periods():
    container_id = request.args.get('container_id')
    if container_id is None:
        abort(404)
    items = RentPeriod.query.filter(RentPeriod.container_id == int(container_id)).order_by(RentPeriod.begin_date).all()
    return render_template('periods.html', items=items)


@app.route('/periods/<int:period_id>/', methods=['GET', 'POST'])
@login_required
def period(period_id=None):
    if period_id is None:
        abort(404)
    period_inst = RentPeriod.query.get(period_id)
    form = RentContainerPeriodForm(obj=period_inst)
    if form.validate_on_submit():
        form.populate_obj(period_inst)
        db.session.add(period_inst)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(u'Произошла ошибка при сохранении периода аренды', 'danger')
        else:
            flash(u'Период аренды контейнера был успешно обновлен', 'success')
            return redirect(url_for('periods', container_id=period_inst.container_id, period_id=period_inst.id))

    return render_template('period.html', form=form, period_id=period_inst.id)


@app.route('/renters/')
@login_required
def renters():
    section = 'renters'
    items = Renter.query.all()
    return render_template('renters.html', items=items, section=section)


@app.route('/renters/add/', methods=['GET', 'POST'])
@app.route('/renters/<int:renter_id>/', methods=['GET', 'POST'])
@login_required
def renter(renter_id=None):
    renter_inst = Renter.query.get(renter_id) if renter_id is not None else Renter()
    form = RenterForm(obj=renter_inst)
    if form.validate_on_submit():
        form.populate_obj(renter_inst)
        db.session.add(renter_inst)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
        else:
            flash(u'Арендатор успешно добавлен' if renter_id is None else u'Арендатор успешно обновлен', 'success')
            return redirect(url_for('renters'))
    return render_template('renter.html', form=form, renter_id=renter_id)


@app.route('/investors/')
@login_required
def investors():
    section = 'investors'
    items = Investor.query.all()
    return render_template('investors.html', items=items, section=section)


@app.route('/investors/add/', methods=['GET', 'POST'])
@app.route('/investors/<int:investor_id>/', methods=['GET', 'POST'])
@login_required
def investor(investor_id=None):
    investor_inst = Investor.query.get(investor_id) if investor_id is not None else Investor()
    form = InvestorForm(obj=investor_inst)
    if form.validate_on_submit():
        form.populate_obj(investor_inst)
        db.session.add(investor_inst)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
        else:
            flash(u'Инвестор успешно добавлен' if investor_id is None else u'Инвестор успешно обновлен', 'success')
            return redirect(url_for('investors'))
    return render_template('investor.html', form=form, investor_id_id=investor_id)


@app.route('/manufacturers/')
@login_required
def manufacturers():
    section = 'manufacturers'
    items = Manufacturer.query.all()
    return render_template('manufacturers.html', items=items, section=section)


@app.route('/manufacturers/add/', methods=['GET', 'POST'])
@app.route('/manufacturers/<int:manufacturer_id>/', methods=['GET', 'POST'])
@login_required
def manufacturer(manufacturer_id=None):
    manufacturer_inst = Manufacturer.query.get(manufacturer_id) if manufacturer_id is not None else Manufacturer()
    form = ManufacturerForm(obj=manufacturer_inst)
    if form.validate_on_submit():
        form.populate_obj(manufacturer_inst)
        db.session.add(manufacturer_inst)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
        else:
            flash(u'Производитель успешно добавлен' if manufacturer_id is None else u'Производитель успешно обновлен', 'success')
            return redirect(url_for('manufacturers'))
    return render_template('manufacturer.html', form=form, manufacturer_id=manufacturer_id)


@app.route('/containers/')
@login_required
def containers():
    section = 'containers'
    items = Container.query.order_by(Container.id).all()
    return render_template('containers.html', items=items, section=section)


@app.route('/containers/add/', methods=['GET', 'POST'])
@app.route('/containers/<int:container_id>/', methods=['GET', 'POST'])
@login_required
def container(container_id=None):
    container_inst = Container.query.get(container_id) if container_id is not None else Container()
    form = ContainerForm(obj=container_inst)
    if form.validate_on_submit():
        form.populate_obj(container_inst)
        db.session.add(container_inst)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
        else:
            flash(u'Блок контейнер успешно добавлен' if container_id is None else u'Блок контейнер успешно обновлен', 'success')
            return redirect(url_for('containers'))
    return render_template('container.html', form=form, container_id=container_id)


@app.route('/period_form/', methods=['GET', 'POST'])
@login_required
def period_form():
    def add_months(sourcedate, months):
        import calendar
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)
    container_id = request.form.get('container_id') or request.args.get('container_id')
    if container_id is None or not container_id.isdigit():
        abort(404)
    period = RentPeriod()
    container = Container.query.get(int(container_id))

    period.begin_date = datetime.date.today()
    period.status = 'open'
    period_form = RentContainerPeriodForm(obj=period)
    if period_form.validate_on_submit():
        period_form.populate_obj(period)
        period.container = container
        period.status = 'open'
        container.status = 'arend'
        rent_period_item = RentPeriodItem()
        rent_period_item.rent_period = period
        rent_period_item.begin_date = period.begin_date
        rent_period_item.end_date = add_months(rent_period_item.begin_date, 1)
        rent_period_item.summ = period.summ
        db.session.add_all([period, container, rent_period_item])
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(u'Произошла ошибка сохранения состояния', 'danger')
        else:
            flash(u'Блок контейнер успешно поставлен в аренду', 'success')
        return 'OK'
    return render_template('ajax/container_period_form.html', form=period_form, container_id=container_id)


@app.route('/edit_month/<int:month_id>/', methods=['GET', 'POST'])
@login_required
def edit_month(month_id):
    month = RentPeriodItem.query.get(month_id)
    form = RentPeriodItemForm(obj=month)
    if form.validate_on_submit():
        form.populate_obj(month)
        db.session.add(month)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash(u'Произошла ошибка сохранения', 'danger')
        else:
            flash(u'Изменения успешно вступили в силу', 'success')
        return redirect(url_for('periods', container_id=month.rent_period.container_id))

    return render_template('month.html', form=form)


@app.route('/end_arend/<int:period_id>/', methods=['GET'])
@login_required
def end_arend(period_id):
    period = RentPeriod.query.get(period_id)
    period.status = 'closed'
    container = period.container
    container.status = 'sklad'
    db.session.add_all([period, container])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(e)
        flash(u'Произошла ошибка сохранения', 'danger')
    else:
        flash(u'Аренда успешно завершена', 'success')
    finally:
        return redirect(url_for('periods', container_id=container.id))


@app.errorhandler(401)
def not_authorized(error):
    return render_template('401.html', error=error), 401


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', error=error), 500


@app.errorhandler(501)
def not_implemented(error):
    return render_template('501.html', error=error), 501
