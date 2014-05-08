__author__ = 'kalyaninirmal'

import couchdb

class CreateDB(object):

    def insertDB(self, user):
       server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
       db = server['python-test']
       doc_id, doc_rev = db.save({'id': user._id, 'name': user._name, 'username': user._username, 'password': user._password})


    def retrieve(self, user):
       print user._username
       server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
       db = server['python-test']
       for dbObj in db:
           doc = db[dbObj]
           print doc['username']
           if doc['username'] == user._username:
               print "*******Existing*******"
               if doc['password'] == user._password:
                    return 1
                    break
               else:
                    return 0
           else:
               print "*******not existing*******"
               return 0
