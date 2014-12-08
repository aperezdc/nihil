#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the MIT license.

import unittest2 as unittest
from .. import headers as H

header_data = (
    (H.Accept("text/plain"),
        "Accept: text/plain\r\n"),
    (H.Authorization("Basic", "payload"),
        "Authorization: Basic payload\r\n"),
    (H.Connection("close"),
        "Connection: close\r\n"),
    (H.Connection("keep-alive"),
        "Connection: keep-alive\r\n"),
    (H.Connection.CLOSE,
        "Connection: close\r\n"),
    (H.Connection.KEEP_ALIVE,
        "Connection: keep-alive\r\n"),
    (H.ContentLength(3245),
        "Content-Length: 3245\r\n"),
    (H.ContentType("text/plain"),
        "Content-Type: text/plain\r\n"),
    (H.Host("some.host.com"),
        "Host: some.host.com\r\n"),
    (H.Host("some.host.com:8888"),
        "Host: some.host.com:8888\r\n"),
    (H.Host("some.other.host.com", 443),
        "Host: some.other.host.com:443\r\n"),
    (H.Location("/"),
        "Location: /\r\n"),
    (H.Location("/local/server/path"),
        "Location: /local/server/path\r\n"),
    (H.Location("http://other.server.com/path"),
        "Location: http://other.server.com/path\r\n"),
    (H.ProxyAuthenticate("Basic", "realm name"),
        "Proxy-Authenticate: Basic realm=realm name\r\n"),
    (H.ProxyAuthorization("Basic", "payload"),
        "Proxy-Authorization: Basic payload\r\n"),
    (H.Server("python-foo/1.4.2"),
        "Server: python-foo/1.4.2\r\n"),
    (H.UserAgent("Mozilla/4.5 (FooBar)"),
        "User-Agent: Mozilla/4.5 (FooBar)\r\n"),
    (H.WWWAuthenticate("Basic", "realm name"),
        "WWW-Authenticate: Basic realm=realm name\r\n"),
    (H.CustomHeader("X-Powered-By", "Batteries!"),
        "X-Powered-By: Batteries!\r\n"),
)


class TestHeaderStringRepresentations(unittest.TestCase):
    @classmethod
    def setup_from_data(cls, data):
        for header, representation in data:
            def f(self):
                self.assertEqual(representation, str(header))
            name = "test_" + header.__class__.__name__ + "_repr"
            count = 0
            while True:
                try_name = "{}_{}".format(name, count)
                count += 1
                if not hasattr(cls, try_name):
                    setattr(cls, try_name, f)
                    break

TestHeaderStringRepresentations.setup_from_data(header_data)


class _TestAuthenticateHeaderBase(object):
    def test_get_set_method(self):
        self.assertEqual("Basic", self.h.method)
        self.h.method = "Digest"
        self.assertEqual("Digest", self.h.method)
        self.assertEqual(self.h.name + ": Digest realm=foorealm\r\n",
                str(self.h))

    def test_get_set_realm(self):
        self.assertEqual("foorealm", self.h.realm)
        self.h.realm = "barbar"
        self.assertEqual("barbar", self.h.realm)
        self.assertEqual(self.h.name + ": Basic realm=barbar\r\n",
                str(self.h))


class TestWWWAuthenticate(unittest.TestCase, _TestAuthenticateHeaderBase):
    def setUp(self):
        self.h = H.WWWAuthenticate("Basic", "foorealm")


class TestProxyAuthenticate(unittest.TestCase, _TestAuthenticateHeaderBase):
    def setUp(self):
        self.h = H.ProxyAuthenticate("Basic", "foorealm")


class _TestAuthorizationHeaderBase(object):
    def test_get_set_method(self):
        self.assertEqual("Basic", self.h.method)
        self.h.method = "Digest"
        self.assertEqual("Digest", self.h.method)
        self.assertEqual(self.h.name + ": Digest xyzpayload\r\n",
                str(self.h))

    def test_get_set_payload(self):
        self.assertEqual("xyzpayload", self.h.payload)
        self.h.payload = "barbar"
        self.assertEqual("barbar", self.h.payload)
        self.assertEqual(self.h.name + ": Basic barbar\r\n",
                str(self.h))

class TestAuthorization(unittest.TestCase, _TestAuthorizationHeaderBase):
    def setUp(self):
        self.h = H.Authorization("Basic", "xyzpayload")


class TestProxyAuthorization(unittest.TestCase,
        _TestAuthorizationHeaderBase):
    def setUp(self):
        self.h = H.ProxyAuthorization("Basic", "xyzpayload")
