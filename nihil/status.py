#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the GPLv3 license.

"""
HTTP status codes.
"""

from .response import Response
from .headers import ContentType, Location
from textwrap import dedent
from string import Template
from six import iteritems, PY3
import re

if PY3:  # pragma: no cover
    from html import escape as html_escape
else:  # pragma: no cover
    from cgi import escape as html_escape

_title_subn = re.compile(r"([^A-Z])([A-Z])").subn
_title_subn_callback = lambda m: m.group(1) + " " + m.group(2)


class cached_result(object):
    __slots__ = ("value", "__name__", "__doc__")
    def __init__(self, func):
        self.value = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
    def __call__(self, obj):
        if callable(self.value):
            self.value = self.value(obj)
        return self.value


class HTTPException(Exception, Response):
    # Those are to be set in subclasses, e.g:
    #   code = 200
    #   explanation = "why this happens"
    code = None
    explanation = ""
    body = Template(dedent("""\
            <html>
             <head>
              <title>${title}</title>
             </head>
             <body>
              <h1>${code} - ${title}</h1>
              <pre>${message}
              ${explanation}</pre>
             </body>
            </html>"""))
    plain_body = Template(dedent("""\
            ${code} - ${title}

            ${message}
            ${explanation}
            """))

    def __init__(self, message=None, comment=None, plaintext=False,
            headers=()):
        if plaintext:
            def render_body():
                yield self.render_plain()
            content_type = ContentType.TEXT_PLAIN
        else:
            def render_body():
                yield self.render_html()
            content_type = ContentType.TEXT_HTML
        Exception.__init__(self, message)
        Response.__init__(self, render_body(), headers + (content_type,))
        self.comment = comment

    @property
    @cached_result
    def title(self):
        title = self.__class__.__name__
        if title.startswith("HTTP"):
            title = title[4:]
        return _title_subn(_title_subn_callback, title)[0]

    @property
    def render_data(self):
        return {
            "code"        : self.code,
            "title"       : self.title,
            "message"     : self.message or "",
            "comment"     : self.comment or "",
            "explanation" : self.explanation,
        }

    def render_html(self):
        if self.body is None:
            return ""
        data = self.render_data
        for k, v in iteritems(data):
            if k != "code":
                data[k] = html_escape(v)
        return self.body.safe_substitute(data)

    def render_plain(self):
        if self.body is None:
            return ""
        return self.plain_body.safe_substitute(self.render_data)

    def __repr__(self):
        return "<HTTP {} {!r}>".format(self.code, self.title)

    def __str__(self):
        return "{} {}\r\n".format(self.code, self.title)


class HTTPError(HTTPException):
    """
    Base class for status codes in the 400 and 500 ranges.
    """


class HTTPRedirect(HTTPException):
    """
    Base class for status codes in the 300 range (redirections).
    """


class HTTPOk(HTTPException):
    """
    Base class for status codes in the 200 range (successful responses).
    """
    code = 200
    title = "OK"


class HTTPCreated(HTTPOk):
    """
    Indicates that the request was fulfilled and a new resource was created.
    """
    code = 201


class HTTPAccepted(HTTPOk):
    """
    Indicates that the request was accepted for processing, but not yet
    completed.
    """
    code = 202
    explanation = "The request is accepted for processing"


class HTTPNonAuthoritativeInformation(HTTPOk):
    """
    Indicates that the metainformation returned is gathered from a third
    party, and not from the origin server.
    """
    code = 203
    title = "Non-Authoritative Information"


class HTTPNoContent(HTTPOk):
    """
    Indicates that the server fulfilled the request bot does not need to
    return data. Metainformation may be updated, though.
    """
    code = 204
    body = None


class HTTPResetContent(HTTPOk):
    """
    Indicates that the server fulfilled the request and the user agent
    should reset the document view which caused the request to be sent.
    """
    code = 205
    body = None


class HTTPPartialContent(HTTPOk):
    """
    Indicates that the server has fulfilled the partial GET request for the
    resource.
    """
    code = 206


class _HTTPMove(HTTPRedirect):
    def __init__(self, message=None, comment=None, location=None,
            plaintext=False, headers=()):
        super(_HTTPMove, self).__init__(message, comment, plaintext, headers
                + (Location(location),))
        self.location = location


class HTTPMultipleChoices(_HTTPMove):
    code = 300


class HTTPMovedPermanently(_HTTPMove):
    code = 301


class HTTPFound(_HTTPMove):
    code = 302
    explanation = "The resource was found at a different location"


class HTTPSeeOther(_HTTPMove):
    code = 303


class HTTPNotModified(HTTPRedirect):
    code = 304
    body = None


class HTTPUseProxy(_HTTPMove):
    code = 305
    explanation = \
            "The resource must be accessed through a proxy\r\n" \
            "indicated at the given location"


class HTTPTemporaryRedirect(_HTTPMove):
    code = 307


class HTTPClientError(HTTPError):
    code = 400
    explanation = \
            "The server could not omply with the request since\r\n" \
            "it is either malformed or otherwise incorrect."


class HTTPBadRequest(HTTPClientError):
    pass


class HTTPUnauthorized(HTTPClientError):
    code = 401
    title = "Unauthorized"
    explanation = \
            "The server could not verify that you are authorized to\r\n" \
            "access the requested document.  Either the supplied\r\n"    \
            "credentials were wrong (e.g., incorrect password), or\r\n"  \
            "your browser does not understand how to supply the\r\n"     \
            "required credentials"


class HTTPPaymentRequired(HTTPClientError):
    code = 402
    title = "Payment Required"
    explanation = "Access was denied for financial reaons"


class HTTPForbidden(HTTPClientError):
    code = 403
    title = "Forbidden"
    explanation = "Access to the requested resource was denied"


class HTTPNotFound(HTTPClientError):
    code = 404
    title = "Not Found"
    explanation = "The requested resource could not be found"


class HTTPMethodNotAllowed(HTTPClientError):
    code = 405
    title = "Method Not Allowed"
    # TODO: Give a good explanation in the body, using the value of
    #       the HTTP method used by the request.


class HTTPNotAcceptable(HTTPClientError):
    code = 406
    title = "Not Acceptable"
    # TODO: Give a good explanation in the body, using the value of
    #       the "Accept" header sent by the user agent.


class HTTPProxyAuthenticationRequired(HTTPClientError):
    code = 407
    explanation = "Authentication with a local proxy is required"


class HTTPRequestTimeout(HTTPClientError):
    code = 408
    title = "Request Timeout"
    explanation = \
            "The server waited too long for the request to\r\n" \
            "be sent by the client."


class HTTPConflict(HTTPClientError):
    code = 409
    title = "Conflict"
    explanation = "There was a conflict when trying to complete the request"


class HTTPGone(HTTPClientError):
    code = 410
    title = "Gone"
    explanation = "The requested resource is no longer available"


class HTTPLengthRequired(HTTPClientError):
    code = 411
    title = "Length Required"
    explanation = "Requred Content-Length header was not sent by client"


class HTTPPreconditionFailed(HTTPClientError):
    code = 412
    title = "Precondition Failed"
    explanation = "Request precondition failed"


class HTTPRequestEntityTooLarge(HTTPClientError):
    code = 413
    title = "Request Entity Too Large"
    explanation = "The body of the request was too large for this server"


class HTTPRequestURITooLong(HTTPClientError):
    code = 414
    #title = "Request URI Too Long"
    explanation = "The request URI was too long for this server"


class HTTPUnsupportedMediaType(HTTPClientError):
    code = 415
    # TODO: Provide a good error message using the value of the
    #       Content-Type header sent by the user agent.


class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    code = 416
    explanation = "The range requested is not available"


class HTTPExpectationFailed(HTTPClientError):
    code = 417


class HTTPUnprocessableEntity(HTTPClientError):
    code = 422
    explanation = "Unable to process the contained instructions"


class HTTPLocked(HTTPClientError):
    # NOTE: From WebDAV.
    code = 423
    explanation = "The resource is locked"


class HTTPFailedDependency(HTTPClientError):
    # NOTE: From WebDAV.
    code = 424
    explanation = \
            "The method could not be performed because the requested\r\n" \
            "action depended on another action and that action failed"


class HTTPPreconditionRequired(HTTPClientError):
    code = 428

