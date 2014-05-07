__author__ = 'kalyaninirmal'

import couchdb


class CreateDB(object):

    def createdb(self,user):
       server = couchdb.Server() #insert hostname and port 5984 if db is not on local machine
       db = server['python-test']
       doc_id, doc_rev = db.save({'type': 'User', 'id': user._id, 'name': user._name, 'username': user._username, 'password': user._password})
       db.view()