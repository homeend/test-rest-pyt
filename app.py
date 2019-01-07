from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resource.item import ItemList, Item
from resource.store import Store, StoreList
from security import identity, auth
from resource.user import UserRegister


def create_app():
    app = Flask(__name__)
    app.secret_key = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = Api(app)

    JWT(app, auth, identity)
    # jwt = JWT(app, auth, identity)

    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserRegister, '/register')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000)
