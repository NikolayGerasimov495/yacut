from flask import flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap
from .utils import create_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        short_id = create_short_link(original_link, custom_id)
        return render_template('index.html', form=form, short_id=short_id)

    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_original_view(short_id):
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)
