__author__ = 'kalyaninirmal'

import couchdb


class CreateDB(object):

    def createdb(self,name,value):
       server = couchdb.Server()
       db = server.create('python-test')
       doc_id, doc_rev = db.save({'type': 'Person', 'name': name})
