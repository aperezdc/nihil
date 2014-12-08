=====
NIHIL
=====
The *Nothing-but-Iffy HTTP I/O Library*
---------------------------------------

NIHIL is a small package which contains utilities to make HTTP services
using the Python ``asyncio`` framework. It provides the following facilities:

* ``Request`` and ``Response`` objects (àla WebOb, but simpler).
* HTTP protocol implementation for ``asyncio``.
* HTTP request parser.
* Request routing.

NIHIL lends itself to be used as a small web framework, by means of the
routing system; or to use the lower level components its parts for other
purposes.

One of the mails goals is to keep the package compatible with both Python
2.7 and 3.x, supporting both CPython and PyPy.
