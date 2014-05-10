import couchdb

class CreateDB(object):

    def insertUserDB(self, user):
        server = couchdb.Server("http://192.168.0.94:5984/")  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        print db.info()
        doc_id, doc_rev = db.save({'id': user._id, 'name': user._name, 'username': user._username, 'password': user._password, 'doc_type':'user'})

    def insertBoard(self, board):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        doc_id, doc_rev = db.save({'boardId': board._boardId, 'boardName': board._boardName, 'userId': board._userId})

    def deleteBoard(self,boardid):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        for dbObj in db:
            print "DB data: ", db
            print "DBObj data: ", dbObj
            doc= db[dbObj]
            if doc['boardId'] == boardid:
                #server.deleteDoc('boards',doc)
                print "deleting doc \n"
                return 1


    def insertPin(self, pin):
        server = couchdb.Server()
        db = server['pins']
        pin_id = db.save({'pinid': pin.pinid,'pinname': pin.pinname, 'pinurl': pin.pinurl, 'boardid':pin.boardid})

    def insertComments(self,comments):
        server = couchdb.Server()
        db = server['comments']
        comment_id = db.save({'comment': comments.comment, 'usercomid':comments.usercomid, 'pinid':comments.pincommentid})

    def retrieve(self, user):
        print user._username
        server = couchdb.Server("http://192.168.0.94:5984")  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
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
        db = server['boards']
        all_boards = []
        for db_object in db:
            doc = db[db_object]
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
        db = server['pins']
        all_pins = []
        for db_object in db:
            doc = db[db_object]
            if doc['board_id'] == board_id:
                    all_pins.append("Pin ID: "+
                                  str(doc['pinid'])+
                                  ", Pin Name: " +
                                  str(doc['pinname']) +", Pin URL: "+str(doc['pinurl'])+ "\n" )
        return all_pins

    def getOnePin(self,pin_id):
        server=couchdb.Server()
        db=server['pins']
        for db_object in db:
            doc=db[db_object]
            if doc['pinid']==pin_id:
                pin_url = str(doc['pinurl'])
            if not pin_url:
                response = ""
            else:
                response = "Pin URL: "+pin_url+" ,"+"\n"+" Comments = ["
                db=server['comments']
                for db_object in db:
                    doc=db[db_object]
                    if doc['pinid']==pin_id:
                        response +="User: "+doc['usercomid']+", Comment: "+doc['comment'] +"\n"
                response += "]\n"
        return response














