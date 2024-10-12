from flask import jsonify, request

from yacut.utils import create_short_link, validate_custom_id

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)

    if 'url' not in data:
        raise InvalidAPIUsage("\"url\" является обязательным полем!", 400)

    custom_id = data.get('custom_id', None)
    validate_custom_id(custom_id)

    url = data['url']
    short_id = create_short_link(url, custom_id)

    return jsonify({
        'url': url,
        'short_link': f'{request.host_url}{short_id}'
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()

    if link is None:
        raise InvalidAPIUsage("Указанный id не найден", 404)

    return jsonify({'url': link.original}), 200
