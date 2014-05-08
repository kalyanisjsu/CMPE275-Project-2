__author__ = 'kalyaninirmal'

import couchdb

class CreateDB(object):

    def insertDB(self, user):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['python-test']
        doc_id, doc_rev = db.save({'id': user._id, 'name': user._name, 'username': user._username, 'password': user._password, 'doc_type':'user'})


    def retrieve(self, user):
        print user._username
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['python-test']
        for dbObj in db:
            doc = db[dbObj]
            if doc['doc_type'] == 'user':
                if doc['username'] == user._username:
                    print "*******Existing*******"
                    if doc['password'] == user._password:
                        return 1
                        break
                else:
                    print "*******not existing*******"


    def getAllBoards(self):
        server = couchdb.Server()
        db = server['python-test']
        all_boards = []
        for db_object in db:
            doc = db[db_object]
            if doc['doc_type'] == 'board':
                all_boards.append("Board ID: "+
                                  str(doc['board_id'])+
                                  ", Board Name: " +
                                  str(doc['board_name']) + "\n" )
        return all_boards

    def getOneBoard (self,board_id):
        server = couchdb.Server()
        db = server['python-test']
        all_pins = []
        for db_object in db:
            doc = db[db_object]
            if doc['doc_type'] == 'pin' and doc['board_id'] == board_id:
                    all_pins.append(str(doc['pin_id']))
        return all_pins
