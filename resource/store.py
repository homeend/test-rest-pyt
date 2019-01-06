from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from model.store import StoreModel


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [store.json() for store in StoreModel.get_all()]}


class Store(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be empty")

    @jwt_required()
    def get(self, name):
        by_name = StoreModel.find_by_name(name)
        if by_name:
            return by_name.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store with name already exists: {}'.format(name)}, 400

        # data = StoreModel.parser.parse_args();
        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        by_name = StoreModel.find_by_name(name)
        if by_name:
            by_name.delete_from_db()
        return {'message': 'Item deleted'}
