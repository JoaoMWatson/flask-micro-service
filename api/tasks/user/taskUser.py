from flask_restful import Resource 
from flask import request

from api.tasks.user.user import user

class taskUser(Resource):

    def __init__(self):
        pass

    def get(self):
        rec = request.get_json(force=True)
        idUser = rec['idUser']

        result = user().testListOfUsers()

        return result
    
    def put(self):
        rec = request.get_json(force=True)

        ID_USER = rec['idUser']
        USER_NAME = rec['userName']
        EMAIL = rec['email']

        result = user().testSaveUser(ID_USER, USER_NAME, EMAIL)

        return result


