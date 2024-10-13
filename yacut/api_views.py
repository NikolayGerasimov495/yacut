from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import create_short_link, validate_custom_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса",
                              HTTPStatus.BAD_REQUEST)

    if 'url' not in data:
        raise InvalidAPIUsage("\"url\" является обязательным полем!",
                              HTTPStatus.BAD_REQUEST)

    custom_id = data.get('custom_id')
    validate_custom_id(custom_id)

    url = data['url']
    short_id = create_short_link(url, custom_id)

    return jsonify({
        'url': url,
        'short_link': f'{request.host_url}{short_id}'
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()

    if link is None:
        raise InvalidAPIUsage("Указанный id не найден",
                              HTTPStatus.NOT_FOUND)

    return jsonify({'url': link.original}), HTTPStatus.OK
