"""

Using bottle (python) RESTful web service.

"""

import time
import sys
import socket
import os
import User
import random
import couchdb

# bottle framework
from bottle import request, response, route, run, template, get, post, error
from couchdatabase import CreateDB

import Board
import Pin

# setup the configuration for our service

def setup(base, conf_fn):
    print '\n**** service initialization ****\n'
    global db, user, signin_done, pin , board
    db = CreateDB()
    user = User.User()
    pin = Pin.Pin()
    signin_done = 0
    board = Board.Board()
	
@route('/')
def root():
    return 'welcome to our website'

@route('/v1/ping', method='GET')
def ping():
    return 'ping %s - %s' % (socket.gethostname(), time.ctime())

@route('/v1/reg', method='POST')
def signup():
    for k, v in request.forms.allitems():
        print "form:", k, "=", v

    id = random.randint(1, 100)
    user._id = id
    user._name = request.forms.get('name')
    user._username = request.forms.get('username')
    user._password = request.forms.get('password')
    return db.insertDB(user)


@route('/v1/login', method='POST')
def signin():
    for k, v in request.forms.allitems():
        print "form:", k, "=", v

    user._username = request.forms.get('username')
    user._password = request.forms.get('password')
    value = db.retrieve(user)
    if value==1:
        return "Login Successful!!!"
    else:
        return "Username doesn't exist or Password is incorrect !!!"

@route('/v1/user/:user_id/board', method='POST')
def createBoard(user_id):
    print "Creating board for user -> " + user_id
    id = random.randint(1, 100)
    board._boardId = id
    print str(board._boardId)
    board._boardName = request.forms.get('boardName')
    board._userId = user_id
    db.insertBoard(board)
    return "Created Board! BoardId : " + str(id) +"\n"

@route('/v1/user/:user_id/board/:board_id', method='POST')
def deleteBoard(user_id,board_id):
    print "Deleting board boardId: " +  str(board_id) +" for user -> " + str(user_id)
    boardid= board_id
    db.deleteBoard(boardid)
    return "Deleting board boardId: " +  str(board_id) +" for user -> " + str(user_id) + "\n"

@route('/v1/boards',method='GET')
def getAllBoards():
    print "get all boards"
    boards = db.getAllBoards()
    print 'all boards from db->',boards
    return boards

@route('/v1/boards/:board_id', method='GET')
def getOneBoard(board_id):
    print 'get one board'
    board = db.getOneBoard()
    print 'all pins in board',board_id, '->', board
    return board

@route('/v1/user/:user_id/pin/upload', method='POST')
def addimage():
    print '--> inside adding image request'
    
    upload = request.files.get('content')
    name, ext = os.path.splitext(upload.filename)

    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    #TODO change this line for windows.

    save_path = '/Users/snehakulkarni/Desktop/275/Project2/save'
    upload.save(save_path)
    addedPinPath = save_path + name
    print addedPinPath

    pin._pinid = '3' #TODO generate the pin id
    pin._pinname = name
    pin._pinurl = addedPinPath
    pin._pincomments = ''

    db.insertPin(pin)

    return 'success'

@route('/v1/pins', method='GET')
def getAllPins():
    print 'Retrieving all pins...'
    pins=db.getAllPins()
    print "All pins ",pins
    return pins

@route('/v1/pins/:pin_id',method='GET')
def getPin():
    print 'Retrieving pin...'
    pin_id=request.GET.get('pin_id')
    pin=db.getOnePin(pin_id)
    return pin


@error(200)
def error200(error1):
    return 'OK'

@error(201)
def error201(error1):
    return 'Created'

@error(204)
def error204(error1):
    return 'No Content'

@error(400)
def error400(error1):
    return 'Bad Request'

@error(401)
def error401(error1):
    return 'Unauthorized'

@error(404)
def error404(error1):
    return 'Not Found'

@error(405)
def error405(error1):
    return 'Method Not Allowed'

@error(500)
def error500(error1):
    return 'Internal Server Error'


# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
#def __format(request):
    #for key in sorted(request.headers.iterkeys()):
    #   print "%s=%s" % (key, request.headers[key])

#    types = request.headers.get("Accept", '')
#    subtypes = types.split(",")
#    for st in subtypes:
#        sst = st.split(';')
#        if sst[0] == "text/html":
#            return Room.html
#        elif sst[0] == "text/plain":
#            return Room.text
#        elif sst[0] == "application/json":
#            return Room.json
#        elif sst[0] == "*/*":
#            return Room.json

            # TODO
            # xml: application/xhtml+xml, application/xml
            # image types: image/jpeg, etc

    # default
#    return Room.html

#
# The content type on the reply
#
#def __response_format(reqfmt):
#    if reqfmt == Room.html:
#        return "text/html"
#    elif reqfmt == Room.text:
#        return "text/plain"
#    elif reqfmt == Room.json:
#        return "application/json"
#    else:
#        return "*/*"

        # TODO
        # xml: application/xhtml+xml, application/xml
        # image types: image/jpeg, etc
