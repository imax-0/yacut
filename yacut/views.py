import random
import string

from flask import render_template, flash, redirect, abort

from . import app, db
from .models import URLMap
from .forms import URLMapForm
from yacut.constants import DEFALUT_SHORT_LINK_ID_LENGTH, FORBIDDEN_SHORT_LINKS


def get_unique_short_id():
    alphabet = string.ascii_letters + string.digits

    def generate_short_id():
        return ''.join(random.choice(alphabet) for _ in range(DEFALUT_SHORT_LINK_ID_LENGTH))

    short_id = generate_short_id()
    while (
        short_id.lower() not in FORBIDDEN_SHORT_LINKS
        and URLMap.query.filter_by(short=short_id).first()
    ):
        short_id = generate_short_id()

    return short_id


@app.route('/', methods=['GET', 'POST'])
def add_short_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data or get_unique_short_id()

        if URLMap.query.filter_by(short=short_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('add_short_link.html', form=form)

        url_map = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('add_short_link.html', form=form, url_map=url_map)

    return render_template('add_short_link.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def short_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)

    return redirect(url_map.original)
