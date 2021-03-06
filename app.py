import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resource.item import ItemList, Item
from resource.store import Store, StoreList
from security import identity, auth
from resource.user import UserRegister


def create_app():
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY', '1234567890')

    app = Flask(__name__)
    app.secret_key = jwt_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = Api(app)

    JWT(app, auth, identity)

    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserRegister, '/register')

    return app


app = create_app()

if __name__ == '__main__':
    from db import db

    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    app.run(port=5000)
