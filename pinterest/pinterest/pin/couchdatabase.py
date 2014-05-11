import couchdb
import json
import random

class CreateDB(object):

    def getAllPins(self):
        """
        1. Get All Pins
        """
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
        return json.dumps(all_pins)

    def getAllBoards(self):
        """
        2. Get All Boards
        """
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

    def getOneBoard (self,board_id):
        """
        3. Get one board
        """
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
        """
        4. Get one pin
        """
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

    def insertUser(self, user):
        """
        5. Registration
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        boards = ['1', '2', '3']
        id = random.randint(1, 100)
        user._id = id
        doc_id, doc_rev = db.save({'id': str(user.id), 'name': user.name, 'username': user.username, 'password': user.password, 'boards': boards})
        return json.dumps(user.__dict__)

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
                    user._id = doc['id']
                    user._password = "****"
                    return json.dumps(user.__dict__)
        user._id = "null"
        user._username = "Wrong Username"
        user._password = "Wrong Password"
        return json.dumps(user.__dict__)

    def retrieveUserBoards(self, user_id):
        """
        7. Get User Boards
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        for dbObj in db:
            doc = db[dbObj]
            uid = doc['id']
            user = {}
            all_boards = []
            if str(user_id) == str(uid):
                #user is found in db
                print "****Success*******"
                user['userName'] = doc['name']
                server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
                db = server['boards']
                for dbObj in db:
                    print '1'
                    #get all boards of user
                    doc = db[dbObj]
                    if str(doc['userId']) == str(user_id):
                        print 'here'
                        board = {}
                        board['board_id'] = doc['board_id']
                        board['board_name'] = str(doc['board_name'])
                        all_boards.append(board)
                result = []
                result.append(user)
                result.append(all_boards)
                return json.dumps(result)
            else:
                print "******Failure******"
                result = []
                return json.dumps(result)

    def insertPin(self, pin):
        """
        8. Upload Pin
        """
        server = couchdb.Server()
        db = server['pins']
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
        return "done"

    def deleteBoard(self,boardid):
        """
        11. Delete Board
        """
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
        #response is status code only

    def insertComments(self,comments):
        """
        12. Add Comment
        """
        server = couchdb.Server()
        db = server['comments']
        comment_id = db.save({'comment': comments.comment, 'usercomid':comments.usercomid, 'pinid':comments.pincommentid})
        #response is status code only
