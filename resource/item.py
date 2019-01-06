from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from model.item import ItemModel


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [u.json() for u in ItemModel.get_all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be empty")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        by_name = ItemModel.find_by_name(name)
        if by_name:
            return by_name.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item with name already exists: {}'.format(name)}, 400

        data = Item.parser.parse_args();
        item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        by_name = ItemModel.find_by_name(name)
        if by_name:
            by_name.delete_from_db()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args();
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()

        return item.json()
