import json, urlparse
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import threading
from cyrusbus import Bus
import os
import logging

bus = 0


class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message = '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
        ])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        self.publish()

        return

    def splitall(self, path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])

        return allparts

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()

        data = json.loads(post_body)

        self.wfile.write(data)
        self.publish(body=data)
        return

    def publish(self, **kwargs):
        parsed_path = urlparse.urlparse(self.path)
        normpath = os.path.normpath(parsed_path.path)
        comps = self.splitall(normpath)
        path_components = filter(lambda item: item != '/', comps)
        bus.publish("web." + path_components[0], path=parsed_path.path, query=parsed_path.query, **kwargs)


class webserver(object):
    """docstring for webserver."""

    def __init__(self, b):
        super(webserver, self).__init__()
        global bus
        bus = b
        self.server = HTTPServer(('0.0.0.0', 8080), GetHandler)

    def start(self):
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.server.shutdown()
