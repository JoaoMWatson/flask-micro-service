from flask_restful import Resource
from flask import request
import json

from api.base.loggerNoSQL import loggerNoSQL

class taskLogger(Resource):

    def __init__(self):
        pass

    def get(self):
        rec = request.get_json(force=True)

        _date = rec['date']
        start = rec['start']
        limit = rec['limit']

        log = loggerNoSQL()
        result = log.testListLogs(_date, start, limit)
        del log

        return result

    def put(self):
        rec = request.get_json(force=True)

        idUser = rec['idUser']
        message = rec['message']
        kind = rec['kind']
        trace = rec['trace']

        log = loggerNoSQL()
        result = log.testAddLog(message, kind, trace, idUser)
        del log
        
        return result

    def post(self):
        return {'message':"error", "result": "POST method not implemented"}, 500

    def delete(self):
        return {'message':"error", "result": "DELETE method not implemented"}, 500
