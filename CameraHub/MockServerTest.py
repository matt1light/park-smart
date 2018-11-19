from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import requests

class MockServerRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        if self.path == "/Images":
            self.send_response(requests.codes.ok)
        else:
            self.send_response(404)
        self.end_headers()
        return
    
    def get_free_port():
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port
    