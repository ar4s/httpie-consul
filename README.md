httpie-consul
=============

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
