#!flask/bin/python
from flask import Flask
import src.sources_controller as sources_controller
app = Flask(__name__)


@app.route('/sources', methods=['GET'])
def sources():
    return sources_controller.get_all()


@app.route('/sources', methods=['POST'])
def create_source():
    sources_controller.new_sources()
    return "pass"


@app.route('/articles')
def articles():
    return "Hier komen de articles"


@app.route('/articles/tfidf')
def articles_tfidf():
    return "Hier komen de tfidf articles"


@app.route('/articles/wordvec')
def articles_wordvec():
    return "Hier komen de wordvec articles "


if __name__ == '__main__':
    app.run(debug=True)
