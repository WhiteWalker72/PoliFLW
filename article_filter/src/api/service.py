from flask import Flask
from src.api import articles_controller
import json

app = Flask(__name__)


@app.route('/articles', methods=['GET'])
def get_articles():
    return json.dumps(articles_controller.get_articles())


def start_api():
    app.run()
