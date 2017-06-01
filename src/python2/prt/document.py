# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from prt.error       import PRTError
from prt.version     import PRTVersion
from prt.v2.document import PRTDocument as _PRTDocumentV2


class PRTDocumentError(PRTError): pass


class InvalidVersion(PRTDocumentError):

    def __init__(self, version=None):
        super(PRTDocumentError, self).__init__(
            'Expected one of {}, but got {!r} ({})'.format(tuple(PRTVersion),
                                                           version,
                                                           version.__class__.__name__))


class PRTDocument(object):
    """
    Version based class dispatcher
    """

    def __new__(self, elements, version=PRTVersion.HIGHEST, *args, **kwargs):
        if version == PRTVersion.V2:
            return _PRTDocumentV2(elements, *args, **kwargs)
        raise InvalidVersion(version)

    @classmethod
    def from_html(cls, string, version=PRTVersion.HIGHEST, *arg, **kwargs):
        if version == PRTVersion.V2:
            return _PRTDocumentV2.from_html(string, *arg, **kwargs)
        raise InvalidVersion(version)

    @classmethod
    def from_json(cls, string, version=PRTVersion.HIGHEST, *arg, **kwargs):
        if version == PRTVersion.V2:
            return _PRTDocumentV2.from_json(string, *arg, **kwargs)
        raise InvalidVersion(version)
