import couchdb

class CreateDB(object):

    def insertDB(self, user):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['python-test']
        doc_id, doc_rev = db.save({'id': user._id, 'name': user._name, 'username': user._username, 'password': user._password, 'doc_type':'user'})

    def insertBoard(self, board):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        doc_id, doc_rev = db.save({'boardId': board._boardId, 'boardName': board._boardName, 'userId': board._userId})

    def deleteBoard(self, board_id):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        for dbObj in db:
            doc= db[dbObj]
            if doc['boardId'] == board_id:
                server.deleteDoc('boards',doc)

    def insertPin(self, pin):
        server = couchdb.Server()
        db = server['python-test']
        pin_id = db.save({'pinid': pin.pinid,'pinname': pin.pinname, 'pinurl': pin.pincomments, 'pincomments':pin.pincomments})

    def insertComments(self,comments):
        server = couchdb.Server()
        db = server['python-test']
        comment_id = db.save({'commentid': comments.commentid, 'comment': comments.comment, 'usercomment':comments.usercomid, 'pincomment':comments.pincommentid})

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


    def getAllPins(self):
        server=couchdb.Server()
        db=server['pins']
        all_pins=[]
        for db_object in db:
            doc=db[db_object]
            all_pins.append("Pin ID: "+
                                  str(doc['pinid'])+
                                  ", Pin Name: " +
                                  str(doc['pinname']) +", Pin URL: "+str(doc['pinurl'])+ "\n" )
        return all_pins

    def getOneBoard (self,board_id):
        server = couchdb.Server()
        db = server['python-test']
        all_pins = []
        for db_object in db:
            doc = db[db_object]
            if doc['doc_type'] == 'pin' and doc['board_id'] == board_id:
                    all_pins.append(str(doc['pin_id']))
        return all_pins

    def getOnePin(self,pin_id):
        server=couchdb.Server()
        db=server['pins']
        for db_object in db:
            doc=db[db_object]
            if doc['pinid']==pin_id:
                pin_url = str(doc['pinid'])
            if not pin_url:
                response = ""
            else:
                response = "Pin URL: "+pin_url+" ,"+"\n"+" Comments = ["
                db=server['comments']
                for db_object in db:
                    doc=db[db_object]
                    if doc['pinid']==pin_id:
                        response +="User: "+doc['usercomid']+", Comment: "+doc['comment'] +"\n"
                response += "]"
        return response














