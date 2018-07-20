"""
Consul plugin for HTTPie.
"""
import os
from urllib.parse import urlparse, urlsplit, urljoin

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


def replace_port(res, port):
    return res._replace()


class ConsulAdapter(HTTPAdapter):
    _consul_client = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._consul_client = Consul(**CONSUL_CLIENT_PARAMS)

    def get_connection(self, url, proxies=None):
        result = urlparse(url)
        service_name = result.netloc
        consul_result = self._consul_client.catalog.service(service_name)
        if not consul_result:
            raise RuntimeError(
                "Consul has returned empty list for {}.".format(service_name)
            )
        result = result._replace(
            scheme=CONSUL_SERVICE_DEFAULT_SCHEMA,
            netloc=':'.join([
                consul_result[0]['Node'],
                str(consul_result[0]['ServicePort'])
            ])
        )
        return super().get_connection(result.geturl(), proxies)


class ConsulPlugin(TransportPlugin):

    name = 'Consul'
    prefix = CONSUL_PREFIX + '://'
    description = 'Add schema additional schema ({}) for Consul.'.format(
        prefix
    )

    def get_adapter(self):
        return ConsulAdapter()
