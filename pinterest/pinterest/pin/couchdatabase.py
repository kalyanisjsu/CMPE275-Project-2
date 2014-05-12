import couchdb
import json
import random
from bottle import HTTPError

class CreateDB(object):

    def getAllPins(self):
        """
        1. Get All Pins
        """
        server=couchdb.Server()
        db=server['pins']
        pins = {}
        all_pins=[]
        for db_object in db:
            doc=db[db_object]
            #Create dictionary object
            pin = {}
            pin['pin_id'] = doc['pinid']
            pin['pin_name'] = str(doc['pinname'])
            pin['pin_url'] = str(doc['pinurl'])
            all_pins.append(pin)
        pins['pins'] = all_pins
        return json.dumps(pins)

    def getAllBoards(self):
        """
        2. Get All Boards
        """
        server = couchdb.Server()
        db = server['boards']
        all_boards = []
        boards = {}
        for db_object in db:
            doc = db[db_object]
            #creating dictionary object
            board = {}
            board['board_id'] = doc['board_id']
            board['board_name'] = str(doc['board_name'])
            all_boards.append(board)
        #return list of dictionaries
        boards['boards'] = all_boards
        return json.dumps(boards)

    def getOneBoard(self,board_id):
        """
        3. Get one board
        """
        server = couchdb.Server()
        db = server['pins']
        all_pins = []
        for db_object in db:
            doc = db[db_object]
            if doc['boardid'] == board_id:
                pin = {}
                pin['pin_id'] = doc['pinid']
                pin['pin_name'] = str(doc['pinname'])
                pin['pin_url'] = str(doc['pinurl'])
                all_pins.append(pin)
        return json.dumps(all_pins)


    def getOnePin(self,pin_id):
        """
        4. Get one pin
        """
        print 'in get one pin'
        pin_url=""
        server=couchdb.Server()
        db=server['pins']
        pin_url =''
        for db_object in db:
            doc=db[db_object]
            if doc['pinid']==pin_id:
                pin_url = str(doc['pinurl'])
                print 'found match'
                break
        if pin_url=="":
            #No Pin found
            print 'No pin found'
            return json.dumps("No pin found")
        else:
            print 'Pin found '+pin_url
            pin={}
            pin['pin_url']=pin_url
            pin['pin_name'] = doc['pinname']
            all_comments=[]
            db=server['comments']
            for db_object in db:
                doc=db[db_object]
                if doc['pinid']==pin_id:
                    comment={}
                    comment['usercomid']=doc['usercomid']
                    print comment['usercomid']
                    comment['comment']=doc['comment']
                    print comment['comment']
                    all_comments.append(comment)
            #result.append(all_comments)

        pin['comments'] = all_comments
        return json.dumps(pin)

    def insertUser(self, user):
        """
        5. Register/Signup User
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        userid_db = 0
        for dbObj in db:
            doc = db[dbObj]
            userid_db = doc['id']
            #print doc
            if doc['username'] == user._username:
                userData = {}
                userData['username'] = "Username already exists !!!"
                return json.dumps(userData)

        user._id = int(userid_db)+1
        doc_id, doc_rev = db.save({'id': str(user.id), 'name': user.name, 'username': user.username, 'password': user.password})
        doc = db[doc_id]
        userData = {}
        userData['user_id'] = doc['id']
        userData['name'] = str(doc['name'])
        userData['username'] = str(doc['username'])
        return json.dumps(userData)

    def retrieveUser(self, user):
        """
        6. Login
        """
        print user._username
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        for dbObj in db:
            doc = db[dbObj]
            print doc
            if doc['username'] == user._username:
                print "*******Existing*******"
                if doc['password'] == user._password:
                     print "*******Existing*******"
                     userData = {}
                     userData['user_id'] = doc['id']
                     userData['name'] = str(doc['name'])
                     userData['username'] = str(doc['username'])
                     return json.dumps(userData)
        #userData = {}
        #userData['user_id'] = "Null"
        #userData['username'] = "Wrong Username"
        #userData['password'] = "Wrong Password"
        #return json.dumps(userData)
        return ""


    def retrieveUserBoards(self, user_id):
        """
        7. Get User Boards #TODO here only one board is returned
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        boards = {}
        all_boards = []
        for dbObj in db:
            doc = db[dbObj]
            uid = doc['userId']
            print "********", doc['userId']
            if str(user_id) == str(uid):
                #user is found in db
                print "****Success*******"
                board = {}
                board['board_id'] = doc['board_id']
                board['board_name'] = str(doc['board_name'])
                all_boards.append(board)
                boards['boards'] = all_boards
        return json.dumps(boards)
        print "******Failure******"
        board = "No boards are created!!"
        return json.dumps(board)

    def insertPin(self, pin):
        """
        8. Upload Pin
        """
        server = couchdb.Server()
        db = server['pins']
        max_id = 0
        for dbObj in db:
            doc = db[dbObj]
            max_id = doc['pinid']
        pin._pinid = int(max_id) + 1
        pin_id = db.save({'pinid': pin.pinid,'pinname': pin.pinname, 'pinurl': pin.pinurl, 'boardid':pin.boardid})
        pin_dict = {}
        pin_dict['pin_id'] = pin.pinid
        return json.dumps(pin_dict)

    def insertBoard(self, board):
        """
        9. Create Board
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        boardid_db = 0
        for dbObj in db:
            doc = db[dbObj]
            boardid_db = doc['board_id']

        board._board_id = int(boardid_db)+1
        doc_id, doc_rev = db.save({'board_id': board._board_id, 'board_name': board._board_name, 'userId': board._userId})
        board_dict = {}
        board_dict['board_id'] = board._board_id
        return json.dumps(board_dict)

    #todo what is the response to be returned? not mentioned in standards doc
    def updatePin(self,pin_id,userid,boardid):
        """
        10. Attach Pin
        """
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
        return self.getOneBoard(boardid)

    def deleteBoard(self,boardid):
        """
        11. Delete Board
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        print "board id: ",boardid
        for dbObj in db:
            print "DB data: ", db
            doc= db[dbObj]
            print "doc data: ", doc
            if str(doc['board_id']) == boardid:
                db.delete(doc)
                print "deleting doc \n"
                return json.dumps("Deleted Board: " + boardid)

    def insertComments(self,comments):
        """
        12. Add Comment
        """
        print "inside add comment"
        server = couchdb.Server()
        db = server['comments']
        comment_id = db.save({'comment': comments.comment, 'usercomid':comments.usercomid, 'pinid':comments.pincommentid})
        return "Don"

    def isvaliduser(self,userid):
        """
        To check if the user id is valid
        """
        server = couchdb.Server()
        db = server['users']
        self.flag = False
        for dbObj in db:
             doc = db[dbObj]
             if str(userid) == str(doc['id']):
                self.flag = True
                break
        return self.flag



