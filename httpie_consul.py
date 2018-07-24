"""
Consul plugin for HTTPie.
"""
import os
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urlparse import urlsplit, urlunsplit

from consulate import Consul
from httpie.plugins import TransportPlugin
from requests.adapters import HTTPAdapter


__version__ = '1.0.2'
__author__ = 'Arkadiusz Adamski'
__licence__ = 'BSD'


CONSUL_SERVICE_DEFAULT_SCHEMA = os.getenv(
    'CONSUL_SERVICE_DEFAULT_SCHEMA', 'http'
)
CONSUL_PREFIX = os.getenv('CONSUL_PREFIX', 'service')
CONSUL_CLIENT_PARAMS = {
    'host': os.getenv('CONSUL_HOST', 'localhost'),
    'port': os.getenv('CONSUL_PORT', 8500),
    'scheme': os.getenv('CONSUL_SCHEME', 'http'),
}


class ConsulAdapter(HTTPAdapter):
    _consul_client = None

    def __init__(self, consul_host=None, consul_port=None, consul_scheme=None, consul_class=None, *args, **kwargs):
        consul_host = consul_host or os.getenv('CONSUL_HOST', 'localhost')
        consul_port = consul_port or os.getenv('CONSUL_PORT', 8500)
        consul_scheme = consul_scheme or os.getenv('CONSUL_SCHEME', 'http'),
        consul_class = consul_class or Consul
        super(ConsulAdapter, self).__init__(*args, **kwargs)
        self._consul_client = consul_class(host=consul_host, port=consul_port)

    def fetch_host_and_port_from_consul(self, service_name):
        consul_result = self._consul_client.catalog.service(service_name)
        if not consul_result:
            raise RuntimeError(
                "Consul has returned empty list for {}.".format(service_name)
            )
        return consul_result[0]['Node'], consul_result[0]['ServicePort']

    def get_connection(self, url, proxies=None):
        (scheme, netloc, path, query, fragment) = urlsplit(url)
        host, port = self.fetch_host_and_port_from_consul(netloc)
        url = urlunsplit((
            CONSUL_SERVICE_DEFAULT_SCHEMA,
            ':'.join((host, str(port))),
            path, query, fragment
        ))
        return super(ConsulAdapter, self).get_connection(url, proxies)


class ConsulPlugin(TransportPlugin):

    name = 'Consul'
    prefix = CONSUL_PREFIX + '://'
    description = 'Add schema additional schema ({}) for Consul.'.format(
        prefix
    )

    def get_adapter(self):
        return ConsulAdapter()
