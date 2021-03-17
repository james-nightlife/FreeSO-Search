from flask import Flask, render_template

from app.blueprints.search_lot import search_lot
from app.blueprints.search_character import search_character
from app.blueprints.search_neighborhood import search_neighborhood
from app.blueprints.creator import creator
from app.blueprints.home import home

from app.config import configurations

def create_app(environment_name='dev'):
    app = Flask(__name__)

    app.config.from_object(configurations[environment_name])

    app.register_blueprint(search_lot)
    app.register_blueprint(search_character)
    app.register_blueprint(search_neighborhood)
    app.register_blueprint(creator)
    app.register_blueprint(home)

    return app

