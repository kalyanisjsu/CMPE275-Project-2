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

    def upload_file(self):
        print '--> i m here 2'
        url = 'http://localhost:8080/moo/pin/add'
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

        conn = httplib.HTTPConnection(netloc)

        data = ''

        try:
            conn.connect()
            conn.putrequest("POST", url)
            conn.putheader('Accept',
                           'image/jpeg')
            conn.putheader('Content-type',
                           'multipart/form-data; boundary=%s'%boundary)
            conn.putheader('Content-length', str(len(body)))
            conn.endheaders()
            conn.send(body)
        except socket.error, e:
            print(str(e), log.ERROR)
            return

        r = conn.getresponse()

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


