__author__ = 'kalyaninirmal'
import couchdb


class CreateDB(object):

    def createdb(self):
       server = couchdb.Server()
       db = server.create('python-tests')
       doc_id, doc_rev = db.save({'type': 'Person', 'name': 'John Doe'})
