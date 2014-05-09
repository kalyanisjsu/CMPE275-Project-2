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

# setup the configuration for our service
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
    save_path = '/Users/poojasrinivas/Desktop/275/Project2/source code/moo-ws/moo/data'
    upload.save(save_path) # appends upload.filename automatically
    addedPinPath = save_path + name;
    #TODO add this to the pin db
    return 'success'

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
