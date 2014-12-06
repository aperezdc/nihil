#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the GPLv3 license.

from codecs import open
from textwrap import dedent
from email import parser, message
from os import path
from re import match


class Metadata(message.Message, object):
    @staticmethod
    def get_author_field(name, field):
        return match(r"^([^<]+)\s+<([^>]*)>$", name).group(field)
    @staticmethod
    def get_multiline(content):
        return [line.strip() for line in content.splitlines() if line]
    @staticmethod
    def get_sub_keyed(content):
        m = parser.Parser().parsestr(content.strip())
        return dict((k, Metadata.get_multiline(m[k])) for k in m.keys())

    description = property(lambda self: self["Description"])
    version = property(lambda self: self["Version"])
    package = property(lambda self: self["Package"])
    url = property(lambda self: self["URL"])
    license = property(lambda self: self["License"])
    main_author_name = property(lambda self:
            self.get_author_field(self.authors[0], 1))
    main_author_email = property(lambda self:
            self.get_author_field(self.authors[0], 2))
    test_requirements = property(lambda self:
            self.get_multiline(self.get("Test-Requirements", "")))
    extra_requirements = property(lambda self:
            self.get_sub_keyed(dedent(self.get("Extra-Requirements", ""))))
    entry_points = property(lambda self:
            self.get_multiline(self.get("Scripts", "")))
    requirements = property(lambda self:
            self.get_multiline(self.get("Requirements", "")))
    classifiers = property(lambda self:
            self.get_multiline(self.get("Classifiers", "")))
    authors = property(lambda self:
            self.get_multiline(self.get("Authors", "")))


def metadata():
    with open(path.join(path.dirname(__file__), "META"), "rU",
            encoding="utf-8") as f:
        return parser.Parser(Metadata).parse(f)
metadata = metadata()
