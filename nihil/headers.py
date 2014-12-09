#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the GPLv3 license.

"""
Utilities to work with HTTP headers.
"""

from six import string_types
from functools import total_ordering


@total_ordering
class Header(object):
    # Name of the header, e.g. Content-Type
    name = None
    single_value = False

    __slots__ = ("_value",)

    def __init__(self, value):
        self._value = value

    def __repr__(self):  # pragma: no cover
        return "<Header:{} {!r}>".format(self.name, self.string_value)

    def __str__(self):
        return "{}: {}\r\n".format(self.name, self.string_value)

    @property
    def string_value(self):
        return str(self._value)

    def __eq__(self, other):
        if isinstance(other, string_types):
            return self.string_value == other
        return self.__class__ is other.__class__ \
           and self._value == other._value

    def __lt__(self, other):
        assert isinstance(other, Header)
        return self.name < other.name \
            or self._value < other._value

    def __iadd__(self, other):
        if isinstance(other, string_types):
            append_value = other
        elif isinstance(other, Header) and self.name == other.name:
            append_value = other.string_value
        else:
            raise ValueError(other)
        self._value = "{}, {}".format(self.string_value, append_value)
        return self


class _StringHeader(Header):
    pass


class CustomHeader(_StringHeader):
    __slots__ = ("name",)

    def __init__(self, name, value):
        super(CustomHeader, self).__init__(value)
        self.name = str(name)


class _NumericHeader(Header):
    def __init__(self, value):
        super(_NumericHeader, self).__init__(int(value))


class _EnumHeader(Header):
    values = ()

    def __init__(self, value=0):
        if isinstance(value, string_types):
            value = self.values.index(value)
        if value >= len(self.values):
            raise ValueError(value)
        super(_EnumHeader, self).__init__(value)

    @property
    def string_value(self):
        return self.values[self._value]


class ContentType(_StringHeader):
    name = "Content-Type"
    single_value = True

ContentType.TEXT_PLAIN = ContentType("text/plain")
ContentType.TEXT_HTML = ContentType("text/html")


class ContentLength(_NumericHeader):
    name = "Content-Length"
    single_value = True


class Connection(_EnumHeader):
    name = "Connection"
    values = ("close", "keep-alive")
    single_value = True

Connection.CLOSE, \
Connection.KEEP_ALIVE \
    = map(Connection, range(len(Connection.values)))


class Host(_StringHeader):
    name = "Host"

    def __init__(self, value, port=None):
        value = str(value)
        if port is not None:
            value = "{}:{}".format(value, int(port))
        super(Host, self).__init__(value)


class UserAgent(_StringHeader):
    name = "User-Agent"


class Server(_StringHeader):
    name = "Server"


class Accept(_StringHeader):
    name = "Accept"


class Authorization(_StringHeader):
    name = "Authorization"

    __slots__ = ("_method",)

    def __init__(self, method, payload):
        super(Authorization, self).__init__(payload)
        self.__set_method(method)

    @property
    def string_value(self):
        return "{} {}".format(self._method, self._value)

    def __get_method(self):
        return self._method
    def __set_method(self, value):
        self._method = str(value)
    method = property(__get_method, __set_method, doc="Authentication method")

    def __get_payload(self):
        return self._value
    def __set_payload(self, value):
        self._value = str(value)
    payload = property(__get_payload, __set_payload,
            doc="Authentication method payload")


class ProxyAuthorization(Authorization):
    name = "Proxy-Authorization"


class WWWAuthenticate(_StringHeader):
    name = "WWW-Authenticate"

    __slots__ = ("_method",)

    def __init__(self, method, realm):
        super(WWWAuthenticate, self).__init__(realm)
        self.__set_method(method)

    @property
    def string_value(self):
        return "{} realm={}".format(self._method, self._value)

    def __get_method(self):
        return self._method
    def __set_method(self, value):
        self._method = str(value)
    method = property(__get_method, __set_method, doc="Authentication method")

    def __get_realm(self):
        return self._value
    def __set_realm(self, value):
        self._value = str(value)
    realm = property(__get_realm, __set_realm, doc="Authentication realm")


class ProxyAuthenticate(WWWAuthenticate):
    name = "Proxy-Authenticate"


class Location(_StringHeader):
    name = "Location"
