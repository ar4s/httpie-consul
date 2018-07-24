import json
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import requests
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler
import multiprocessing

from httpie_consul import ConsulAdapter


class MockedService(HTTPServer):
    pass


def get_handler_class_for_service(response_text=b'My Fancy Service!', status_code=200):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(status_code)
            self.end_headers()
            self.wfile.write(response_text)
    return Handler

def get_handler_class_for_consul(response_json, status_code=200):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(status_code)
            self.end_headers()
            self.wfile.write(json.dumps(response_json).encode())
    return Handler


class ConsulAdapterTest(unittest.TestCase):
    consul_host = service_host = 'localhost'
    service_port = 8080
    consul_port = 8500
    service_process = None
    consul_process = None

    def tearDown(self):
        if self.service_process:
            self.service_process.terminate()

        if self.consul_process:
            self.consul_process.terminate()

    def start_service(self, handler_class):
        server = MockedService((self.service_host, self.service_port), handler_class)
        self.service_process = multiprocessing.Process(target=server.serve_forever)
        self.service_process.start()

    def start_consul(self, handler_class):
        server = MockedService((self.consul_host, self.consul_port), handler_class)
        self.consul_process = multiprocessing.Process(target=server.serve_forever)
        self.consul_process.start()

    def test_resolve_service_name(self):
        self.start_service(get_handler_class_for_service())
        self.start_consul(get_handler_class_for_consul([{
            'Node': self.service_host,
            'ServicePort': self.service_port
        }]))
        session = requests.Session()
        session.mount('service://', ConsulAdapter(consul_host=self.consul_host, consul_port=self.consul_port))
        session.get('service://test')
