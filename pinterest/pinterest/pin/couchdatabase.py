import couchdb
import json
import random

class CreateDB(object):

    def insertUser(self, user):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        boards = ['1', '2', '3']
        id = random.randint(1, 100)
        user._id = id
        doc_id, doc_rev = db.save({'id': str(user.id), 'name': user.name, 'username': user.username, 'password': user.password, 'boards': boards})
        return json.dumps(user.__dict__)
    def insertBoard(self, board):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        doc_id, doc_rev = db.save({'board_id': board._board_id, 'board_name': board._board_name, 'userId': board._userId})

    def deleteBoard(self,boardid):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        for dbObj in db:
            print "DB data: ", db
            print "DBObj data: ", dbObj
            doc= db[dbObj]
            if doc['board_id'] == boardid:
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

    def retrieveUser(self, user):
        print user._username
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        print "I am here"
        db = server['users']
        print "im here 2"
        for dbObj in db:
            doc = db[dbObj]
            print doc
            if doc['username'] == user._username:
                print "im here 3"
                print "*******Existing*******"
                if doc['password'] == user._password:
                    user._id = doc['id']
                    user._password = "****"
                    return json.dumps(user.__dict__)
        user._id = "null"
        user._username = "Wrong Username"
        user._password = "Wrong Password"
        return json.dumps(user.__dict__)


    def retrieveUserBoards(self, user_id):
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        for dbObj in db:
            doc = db[dbObj]
            print doc['id']
            uid = doc['id']
            if str(user_id) == str(uid):
                print "****Success*******"
                #print doc['board']
                server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
                db = server['boards']
                for dbObj in db:
                    doc = db[dbObj]
                    print doc['name']
            else:
                print "******Failure******"


    def getAllBoards(self):
        server = couchdb.Server()
        db = server['boards']
        all_boards = []
        for db_object in db:
            doc = db[db_object]
            #creating dictionary object
            board = {}
            board['board_id'] = doc['board_id']
            board['board_name'] = str(doc['board_name'])
            all_boards.append(board)
        #return list of dictionaries
        return json.dumps(all_boards)


    def getAllPins(self):
        server=couchdb.Server()
        db=server['pins']
        all_pins=[]
        for db_object in db:
            doc=db[db_object]
            #Create dictionary object
            pin = {}
            pin['pin_id'] = doc['pinid']
            pin['pin_name'] = str(doc['pinname'])
            pin['pin_url'] = str(doc['pinurl'])
            all_pins.append(pin)
            # all_pins.append("Pin ID: "+
            #                       str(doc['pinid'])+
            #                       ", Pin Name: " +
            #                       str(doc['pinname']) +", Pin URL: "+str(doc['pinurl'])+ "\n" )
        return json.dumps(all_pins)

    def getOneBoard (self,board_id):
        server = couchdb.Server()
        db = server['pins']
        all_pins = []
        for db_object in db:
            doc = db[db_object]
            if doc['board_id'] == board_id:
                pin = {}
                pin['pin_id'] = doc['pinid']
                pin['pin_name'] = str(doc['pinname'])
                pin['pin_url'] = str(doc['pinurl'])
                all_pins.append(pin)
        return json.dumps(all_pins)

#todo create response object
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

    def updatePin(self,pin_id,userid,boardid):
        print "inside the updatePin"
        server=couchdb.Server()
        db=server['pins']
        for db_object in db:
            doc=db[db_object]
            print 'the pin_id %s' % pin_id
            print 'the doc pin_id %s' %doc['pinid']
            if doc['pinid']== pin_id:
                print '** inside the pin id if** '
                boards = doc['boardid']
                boards.append(boardid)
                doc['boardid'] = boards
                print type(doc)
                db.save(doc)
        return "done"














