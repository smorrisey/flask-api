from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    parser = reqparse.RequestParser()
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message' : 'store not found'}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'message': "a store with '{}' already exists".format(name)}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': "An error occoured, failed to insert store into database"}, 500 #internal server error

        return store.json(), 201
        

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return{'message': 'store deleted'}        


class StoreList(Resource):
    
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
