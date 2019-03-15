from flask import Flask
from flask import request
from src.api import sources_controller
import src.api.rest_utils as rest_utils
import json

app = Flask(__name__)


def get_error(code, message):
    return {'code': code, 'message': message}


@app.route('/sources', methods=['GET', 'POST'])
def get_sources():
    if request.method == 'GET':
        return json.dumps(sources_controller.get_sources())
    elif request.method == 'POST':
        data = request.form
        return json.dumps(sources_controller.add_source(data['url']))
    else:
        return rest_utils.get_error(405, 'Method not allowed')


@app.route('/sources/<url>', methods=['DELETE'])
def delete_source():
    url = request.args.get('url')
    if request.method == 'DELETE':
        return json.dumps(sources_controller.delete_source(url))
    else:
        return rest_utils.get_error(405, 'Method not allowed')


def start_api():
    app.run()
