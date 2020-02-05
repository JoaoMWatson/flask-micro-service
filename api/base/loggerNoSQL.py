from datetime import datetime
import unittest

from pymongo import MongoClient, errors
import traceback


class loggerNoSQL(unittest.TestCase):
    def __init__(self):
        """
        Classe que escreve e le logging de qualquer tipo, informação ou erro da aplicação
        classe principal que vai prover todos os metodos de conexão e teste
        """

        self.client = MongoClient(
            "mongodb+srv://uselessguy:senhasenha@cluster0-dcwas.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.idsInserted = []

        self.__testConnection()

        self.__listOfLogs = []

    def checkServer(self):
        """ 
        Tenta se conectar a instancia do MongoDB Cloud e tenta criar coleções
        Retorno: Verdadeiro se o banco de dados foi acessado e Falso caso encontre qualquer outro problema 
        """
        try:
            self.client.server_info()
            self.db = self.client.logRecipe
            self.__startTables()

            return True
        except:
            return False

    def __testConnection(self):
        """
        Testa o metodo checkServer para conectar com o banco de dados
        """

        try:
            self.assertTrue(self.checkServer(), True)
        except AssertionError as ae:
            raise Exception(f"Erro ao conectar com o banco de dados: [{ae}]")

    def __startTables(self):
        """
        Começa a criar coelçoes de tabelas se não foram criadas ainda
        """

        tables = [{"tableName": "tb_logInfo",
                   "firstRec": {
                       "ID_USER": 1,
                       "DATE_OF": datetime.now().strftime('%m/%d/%Y %H:%M'),
                       "MESSAGE": "Test log",
                       "LEVEL": "Info",
                       "TRACE": "Empty"
                   }
                   }, {"tableName": "tb_user",
                       "firstRec": {
                           "ID_USER": 1,
                           "EMAIL": "joaopedro.wat22@gmail.com",
                           "NAME": "João Pedro"
                       }
                       }]

        for item in tables:
            self.__createTable(item['tableName'], item['firstRec'])

    def __createTable(self, tableName, firstRec):
        """
        Checa se o 'tableName' ja existe e cria a tabela com os campos
        descritos na variavel 'firstRec'

        Retorno:
            retorna 'True' se a tablea foi criada com sucesso
        """

        if tableName not in self.db.collection_names():
            tbl = self.db[tableName]
            tbl.insert_one(firstRec)
            tbl.delete_one(firstRec)

            return True

        return False

    def addLog(self, message, kind, trace, idUser):
        """
        Cria um novo log de informação ou erro e inseri no banco de dados
        """

        td_logInfo = self.db.td_logInfo

        result = td_logInfo.insert_one({
            "ID_USER": idUser,
            "DATE_OF": datetime.now().strftime('%m/%d/%Y %H:%M'),
            "MESSAGE": message,
            "LEVEL": kind,
            "TRACE": trace,
        })

        return result._WriteResult__acknowledged

    def testAddLog(self, message, kind, trace, idUser):
        """
        Teste o metodo addLog

        Retorno: returna o numero da insersão. 
            Uma gravação sera inserida por padrão
        """

        try:
            self.assertGreater(self.addLog(message, kind, trace, idUser), 0)

            return {"message": "ok", "result": "1 record of logging was inserted on the database"}, 200
        except AssertionError as ae:
            return {"message": "Error", "result": f"[{ae}]"}, 500

    def listLogs(self, _date, start, limit):
        """
        Cria uma lista filtrada da coleção de logs

        Retorno: retorna a quantiade de logs achados
        """

        tb_logInfo = self.db.td_logInfo

        recipes = tb_logInfo.find({
            "DATE_OF": {'$gt': _date}
        }).sort("DATE_OF", -1).skip(start).limit(limit)

        for item in recipes:
            self.__listOfLogs.append(
                (item["DATE_OF"], item['LEVEL'], item['MESSAGE'], item['TRACE']))

        return len(self.__listOfLogs)

    def testListLogs(self, data, start, limit):
        """
        Testa a lista de logs

        Retorno: retorna a lista de logs preenchida 
        """

        try:
            self.assertGreater(self.listLogs(data, start, limit), 0)

            return {"message": "Ok", "result": self.__listOfLogs}, 200
        except AssertionError as ae:
            return {"message": "Error", "result": f"[{ae}]"}, 500
