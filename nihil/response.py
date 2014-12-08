#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the GPLv3 license.

"""
The Response object.
"""

from six import text_type


class Response(object):
    """
    Represents a HTTP response given to a client.
    """
    def __init__(self, body=(), headers=()):
        if isinstance(body, text_type):
            def f():
                yield body
            body = f()

        self.__body_iter = body
        self.headers = headers

    def __iter__(self):
        for x in self.headers:
            yield str(x)
        yield "\r\n"
        for x in self.__body_iter:
            yield x
