"""
6, Apr 2013

Example bottle (python) RESTful web service.

This example provides a basic setup of a RESTful service

Notes
1. example should perform better content negotiation. A solution is
   to use minerender (https://github.com/martinblech/mimerender)
"""

import time
import sys
import socket
import User
import random

import couchdb


# bottle framework
from bottle import request, response, route, run, template, get, post, error

# moo
from classroom import Room
from couchdatabase import CreateDB

# virtual classroom implementation
room = None


def setup(base, conf_fn):
    print '\n**** service initialization ****\n'
    global room, db, user
    room = Room(base, conf_fn)
    db = CreateDB()
    user = User.User()

#
# setup the configuration for our service
@route('/')
def root():
    print "--> root"
    return 'welcome'


#
#
@route('/moo/ping', method='GET')
def ping():
    return 'ping %s - %s' % (socket.gethostname(), time.ctime())


#
# Development only: echo the configuration of the virtual classroom.
#
# Testing using curl:
# curl -i -H "Accept: application/json" http://localhost:8080/moo/conf
#
# WARN: This method should be disabled or password protected - dev only!
#
@route('/moo/conf', method='GET')
def conf():
    fmt = __format(request)
    response.content_type = __response_format(fmt)
    return room.dump_conf(fmt)


#
# example of a RESTful method. This example is very basic, it does not 
# support much in the way of content negotiation.
#
@route('/moo/echo/:msg')
def echo(msg):
    fmt = __format(request)
    response.content_type = __response_format(fmt)
    if fmt == Room.html:
        return '<h1>%s</h1>' % msg
    elif fmt == Room.json:
        rsp = {}
        rsp["msg"] = msg
        return json.dumps(all)
    else:
        return msg


@route('/moo/hello')
def hello():
    return "Hello World!"


@route('/v1/reg', method='POST')
def signup():
    for k, v in request.forms.allitems():
        print "form:", k, "=", v

    id = random.randint(1, 100)
    user._id = id
    user._name = request.forms.get('name')
    user._username = request.forms.get('username')
    user._password = request.forms.get('password')
    return db.createdb(user)


#
# example of a RESTful query
#
@route('/moo/data/:name', method='GET')
def find(name):
    print '---> moo.find:', name
    return room.find(name)


#
# example adding data using forms
#
@route('/moo/data', method='POST')
def add():
    print '---> moo.add'

    # example list form values
    for k, v in request.forms.allitems():
        print "form:", k, "=", v

    name = request.forms.get('name')
    value = request.forms.get('value')
    return room.add(name, value)

# Error code - added by Kalyani

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

#
# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
def __format(request):
    #for key in sorted(request.headers.iterkeys()):
    #   print "%s=%s" % (key, request.headers[key])

    types = request.headers.get("Accept", '')
    subtypes = types.split(",")
    for st in subtypes:
        sst = st.split(';')
        if sst[0] == "text/html":
            return Room.html
        elif sst[0] == "text/plain":
            return Room.text
        elif sst[0] == "application/json":
            return Room.json
        elif sst[0] == "*/*":
            return Room.json

            # TODO
            # xml: application/xhtml+xml, application/xml
            # image types: image/jpeg, etc

    # default
    return Room.html


#
# The content type on the reply
#
def __response_format(reqfmt):
    if reqfmt == Room.html:
        return "text/html"
    elif reqfmt == Room.text:
        return "text/plain"
    elif reqfmt == Room.json:
        return "application/json"
    else:
        return "*/*"

        # TODO
        # xml: application/xhtml+xml, application/xml
        # image types: image/jpeg, etc
