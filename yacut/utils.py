import random
import re
from http import HTTPStatus

from flask import flash

from . import db
from .constants import (CHARACTER_SET, CUSTOM_ID_REGEX,
                        DEFAULT_SHORT_ID_LENGTH, MAX_CUSTOM_ID_LENGTH)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_custom_id(custom_id):
    if custom_id:
        if (not re.match(CUSTOM_ID_REGEX, custom_id) or len(custom_id)
            > MAX_CUSTOM_ID_LENGTH):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки",
                HTTPStatus.BAD_REQUEST)

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует.",
                HTTPStatus.BAD_REQUEST)


def get_unique_short_id(length=DEFAULT_SHORT_ID_LENGTH):
    characters = CHARACTER_SET
    while True:
        short_id = ''.join(random.choices(characters, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def create_short_link(original_url, custom_id=None):
    if (custom_id and URLMap.query.filter_by(short=custom_id).first() is
            not None):
        raise InvalidAPIUsage(
            "Предложенный вариант короткой ссылки уже существует.",
            HTTPStatus.BAD_REQUEST)

    short_id = custom_id if custom_id else get_unique_short_id()

    new_link = URLMap(original=original_url, short=short_id)
    db.session.add(new_link)
    db.session.commit()

    return short_id
