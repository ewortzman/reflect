#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Written by Nathan Hamiel (2010)

import collections
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
from pprint import pprint, pformat

import time
import random

class RequestHandler(BaseHTTPRequestHandler):
    delay = False

    def do_GET(self):
        if RequestHandler.delay:
            time.sleep(random.random()*2+1)

        request_path = self.path

        print "----- Request Start -----"
        print(request_path)
        print(self.headers)
        print "-------------------------"

        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        print "------ Request End ------\n\n"

    def do_POST(self):

        if RequestHandler.delay:
            time.sleep(random.random()*2+1)

        request_path = self.path

        print "----- Request Start -----"
        print(request_path)

        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0

        print(request_headers)

        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            data = pformat(convert(data))
        except Exception as e:
            data = body
        print data
        print "-------------------------"

        self.send_response(200)
        print "------ Request End ------\n\n"

    do_PUT = do_POST
    do_DELETE = do_GET
    do_HEAD = do_GET

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def main(options, args):
    port = int(options.port) or 8081
    if options.delay:
        RequestHandler.delay = True
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
            "Run:\n\n"
            "   reflect")
    parser.add_option('-p','--port',dest='port',help='what port to run on',default=8081)
    parser.add_option('-d','--delay',dest='delay',help='add a delay to the response',action='store_true',default=False)
    (options, args) = parser.parse_args()
    try:
        main(options, args)
    except KeyboardInterrupt:
        print "Thanks for playing!"
        exit();
