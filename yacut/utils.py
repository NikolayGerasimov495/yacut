import random
import re
import string

from flask import flash

from . import db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_custom_id(custom_id):
    if custom_id:
        if not re.match(r'^[a-zA-Z0-9]+$', custom_id) or len(custom_id) > 16:
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки",
                400)

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует.",
                400)


def get_unique_short_id(existing_ids, length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=length))
        if short_id not in existing_ids:
            return short_id


def create_short_link(original_url, custom_id=None):
    existing_ids = {link.short for link in URLMap.query.all()}
    short_id = custom_id if custom_id else get_unique_short_id(existing_ids)

    new_link = URLMap(original=original_url, short=short_id)
    db.session.add(new_link)
    db.session.commit()

    return short_id
