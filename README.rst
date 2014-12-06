======
Mohawk
======

Mohawk stads for *My Own HTTP Asyncio Web Kit*. It is a small package
with utilities to make HTTP services using the ``asyncio`` framework.
It provides the following facilities:

* ``Request``, ``Response`` objects (àla WebOb, but simpler).
* HTTP protocol implementation for ``asyncio``.
* HTTP request parser.
* Request routing.

Mohawk lends itself to be used as a small web framework, by means of the
routing system; or to use the lower level components its parts for other
purposes.

One of the mails goals is to keep the package compatible with both Python
2.7 and 3.x, supporting both CPython and PyPy.
