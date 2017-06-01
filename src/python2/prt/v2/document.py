# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from json        import (dumps,
                         loads)
from collections import OrderedDict
from lxml.html   import (Element,
                         tostring,
                         fromstring)

from prt.error      import PRTError
from prt.version    import PRTVersion
from prt.v2.mark_up import PRTMarkUp


class PRTDocumentError(PRTError)            : pass
class InvalidPRTDocument(PRTDocumentError)  : pass
class IncompatibleVersion(PRTDocumentError) : pass
class IncompatibleDialect(PRTDocumentError) : pass


class PRTDocument(object):
    """
    Usage:
        >>> from prt import PRTDocument
        >>> from prt.v2.pop_dialect import PRTPOPDialect

        # Create from python objects
        >>> document = PRTDocument([(0x00, {'href': '#'}, 'click')], dialect=PRTPOPDialect)
        >>> document.to_json()
        '{"type":"PRTDocument","version":"2.0","dialect":"pop","elements":[[0,{"href":"#"},"click"]]}'
        >>> document.to_html()
        '<PRTDocument version="2.0" dialect="pop"><a href="#">click</a></PRTDocument>'

        # Create from HTML string
        >>> PRTDocument.from_html('<img src="img.png">', dialect=PRTPOPDialect).to_json()
        '{"type":"PRTDocument","version":"2.0","dialect":"pop","elements":[[11,{"src":"img.png"},null]]}'

        # Create from JSON string
        >>> PRTDocument.from_json('[[1, null, "text"]]', dialect=PRTPOPDialect).to_html()
        '<PRTDocument version="2.0" dialect="pop"><b>text</b></PRTDocument>'
    """

    _VERSION = PRTVersion.V2

    def __init__(self, elements, dialect=None):
        self._dialect = dialect
        self._mark_up = PRTMarkUp(elements, dialect)

    @staticmethod
    def _from_etree(document, dialect):
        elements = []
        for etree in document:
            identifier = dialect.identifier_from_html(etree.tag)
            attributes = dict(dialect.attribute_from_html(identifier, *map(unicode, a))
                for a in etree.attrib.iteritems()) or None
            if not len(etree):
                if etree.text:
                    elements_ = unicode(etree.text)
                else:
                    elements_ = None
            else:
                elements_ = PRTDocument._from_etree(etree, dialect)
            elements.append((identifier, attributes, elements_))
        return elements

    @classmethod
    def from_html(cls, string, dialect=None):
        document = fromstring(string)
        if document.tag != 'prtdocument':
            raise InvalidPRTDocument
        elif document.get('version', None) != cls._VERSION.value:
            raise IncompatibleVersion
        elif document.get('dialect', None) != dialect.name:
            raise IncompatibleDialect

        return PRTDocument(cls._from_etree(document, dialect), dialect)

    @classmethod
    def from_json(cls, string, dialect=None):
        document = loads(string, object_pairs_hook=OrderedDict)
        if document.get('type', None) != 'PRTDocument':
            raise InvalidPRTDocument
        elif document.get('version', None) != cls._VERSION.value:
            raise IncompatibleVersion
        elif document.get('dialect', None) != dialect.name:
            raise IncompatibleDialect

        return PRTDocument(document.get('elements', None), dialect)

    def to_html(self):
        self.validate()
        document = Element('PRTDocument')
        document.set('version', self._VERSION.value)
        if self._dialect:
            document.set('dialect', self._dialect.name)
        self._mark_up.append_to_etree(document)
        return tostring(document)

    def to_json(self):
        """
        JSON representation of the PRTDocument
        """
        self.validate()
        document = OrderedDict()
        document['type'] = 'PRTDocument'
        document['version'] = self._VERSION.value
        if self._dialect:
            document['dialect'] = self._dialect.name
        document['elements'] =self._mark_up.elements()
        return dumps(document, separators=(',', ':'))

    def __nonzero__(self):
        return bool(self._mark_up)

    def __eq__(self, other):
        try:
            return (self.__class__ is other.__class__ and
                    self._mark_up == other._mark_up)
        except PRTError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def validate(self):
        self._mark_up.validate()

    __repr__ = to_html
    __str__  = to_json
