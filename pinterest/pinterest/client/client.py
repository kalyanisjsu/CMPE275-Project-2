import os
import socket
import zipfile
import httplib
import base64
import urlparse
import tempfile
import sys
import urllib2
import mimetypes
from distutils import log
from bottle import run

try:
    bytes
except NameError:
    bytes = str


def b(str_or_bytes):
    if not isinstance(str_or_bytes, bytes):
        return str_or_bytes.encode('ascii')
    else:
        return str_or_bytes

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class ClientPy:

    def __init__(self):
        if len(sys.argv) > 1:
          self.host = sys.argv[1]
          self.url = ''
          self.flg = False
          cmd = self.printusage()
          while(cmd <> '0'):
                if cmd == '1':
                    self.signUp()
                    cmd = self.printusage()
                elif cmd == '2':
                    self.signIn()
                    cmd = self.printusage()
                elif cmd == '3':
                    self.getAllBoards()
                    cmd = self.printusage()
                elif cmd == '4':
                    self.getAllPins()
                    cmd = self.printusage()
                elif cmd == '5':
                    inboardid = raw_input('\nEnter the Board Id :')
                    self.getBoard(inboardid)
                    cmd = self.printusage()
                elif cmd == '6':
                    inpinid = raw_input('\nEnter the Board Id :')
                    self.getPin(inpinid)
                    cmd = self.printusage()
                elif cmd > 6 :
                    if(self.flg):
                        if cmd == '7':
                            self.getUserBoard()
                            cmd = self.printusage()
                        elif cmd == '8':
                            self.UploadPin()
                            cmd = self.printusage()
                        elif cmd == '9':
                            self.createBoard()
                            cmd = self.printusage()
                        elif cmd == '10':
                            self.attachPin()
                            cmd = self.printusage()
                        elif cmd == '11':
                            self.addComment()
                            cmd = self.printusage()
                        elif cmd == '12':
                            self.deleteBoard()
                            cmd = self.printusage()
                        elif cmd > '12':
                            print "Please enter correct option!!!!"
                            cmd = self.printusage()
                    else:
                        print "Please enter correct option and Login for more functionalities"
                        cmd = self.printusage()
          self.quitConnection()
        else:
          print "usage:", sys.argv[0],"[host ip] example 'x.x.x.x.'"

    def printusage(self):
        if(self.flg):
          print "Press the Key of Choice" \
                "\n1. Registration" \
                "\n2. Login" \
                "\n3. See All Boards" \
                "\n4. See All Pins" \
                "\n5. Get a Board with Boardid as arg" \
                "\n6. Get a Pin with Pinid as arg" \
                "\n7. Get UserBoard" \
                "\n8. Upload pin" \
                "\n9. Create Board" \
                "\n10.Attach Pin" \
                "\n11.Add Comment" \
                "\n12.Delete Board" \
                "\n0. Quit"
        else:
          print "Press the Key of Choice" \
                "\n1. Registration" \
                "\n2. Login" \
                "\n3. See All Boards" \
                "\n4. See All Pins" \
                "\n5. Get a Board with Boardid as arg" \
                "\n6. Get a Pin with Pinid as arg" \
                "\n0. Quit"

        cmd = raw_input("\nEnter option :")
        return cmd

    def signUp(self):
        self.flg = True
        return

    def signIn(self):
        self.flg = True
        return

    def getAllBoards(self):
        return

    def getAllPins(self):
        return

    def getBoard(self,board_id):
        return

    def getPin(self,pin_id):
        return

    def quitConnection(self):
        self.conn.close()
        return

    def getUserBoard(self):
        return

    def UploadPin(self):
        return

    def createBoard(self):
        return

    def attachPin(self):
        return

    def addComment(self):
        return

    def deleteBoard(self):
        return

    def upload_file(self):
        print '--> i m here 2'
        url = 'http://localhost:8080/v1/user/45/pin/upload'
        filename = 'image.jpg'
        #files = {'file': open('image.jpg', 'rb')}
        content = open(filename, 'rb').read()

        data = {
            ':action': 'doc_upload',
            'content': (os.path.basename(filename), content),
        }

        boundary = b('--------------GHSKFJDLGDS7543FJKLFHRE75642756743254')
        sep_boundary = b('\n--') + boundary
        end_boundary = sep_boundary + b('--')
        body = []

        for key, values in data.items():
            # handle multiple entries for the same name
            if type(values) != type([]):
                values = [values]
            for value in values:
                if type(value) is tuple:
                    fn = b(';filename="%s"' % value[0])
                    value = value[1]
                else:
                    fn = b("")
                body.append(sep_boundary)
                body.append(b('\nContent-Disposition: form-data; name="%s"'%(key)))
                body.append(fn)
                body.append(b("\n\n"))
                body.append(b(value))
                if value and value[-1] == b('\r'):
                    body.append(b('\n'))  # write an extra newline (lurve Macs)
        body.append(end_boundary)
        body.append(b("\n"))
        body = b('').join(body)


        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(url)

        self.conn = httplib.HTTPConnection(netloc)

        data = ''

        try:
            self.conn.connect()
            self.conn.putrequest("POST", url)
            self.conn.putheader('Accept',
                           'image/jpeg')
            self.conn.putheader('Content-type',
                           'multipart/form-data; boundary=%s'%boundary)
            self.conn.putheader('Content-length', str(len(body)))
            self.conn.endheaders()
            self.conn.send(body)
        except socket.error, e:
            print(str(e), log.ERROR)
            return

        r = self.conn.getresponse()

        if r.status == 200:
            print('Server response (%s): %s') % (r.status, r.reason)

        elif r.status == 301:
            location = r.getheader('Location')
            if location is None:
                location = 'http://packages.python.org/%s/' % meta.get_name()
            print('Upload successful. Visit %s') % (location)
        else:
            print('Upload failed (%s): %s') % (r.status, r.reason)

        print '-'*75, r.read(), '-'*75

if __name__ == "__main__":
    sam = ClientPy()
    sam.upload_file()


