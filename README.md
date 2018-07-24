httpie-consul
=============
![Travis (.org)](https://img.shields.io/travis/ar4s/httpie-consul.svg)
![PyPI](https://img.shields.io/pypi/v/httpie-consul.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/httpie-consul.svg)
![PyPI - License](https://img.shields.io/pypi/l/httpie-consul.svg)

Consul plugin for [HTTPie](https://httpie.org/).

It currently provides support for Consul.


Installation
------------

```bash
    $ pip install httpie-consul
```

You should now use plugin.


Usage
-----

```bash
    $ http service://my-fancy-service/
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 32

    Response from My Fancy Service!
```

You can also configure plugin by environment variables:

```bash
    $ export CONSUL_HOST=consul.local
    $ export CONSUL_PORT=80
    $ export CONSUL_SCHEME=https
```
