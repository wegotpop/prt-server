# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from PRT modules
from prt.error       import PRTError
from prt.version     import PRTVersion, InvalidVersion
from prt.dialects    import get_dialect
from prt.v2.document import PRTDocument as _PRTDocumentV2


#------------------------------------------------------------------------------#
class PRTDocument(object):
    """
    Version based class dispatcher
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __new__(cls, elements,
                     dialect,
                     version=PRTVersion.HIGHEST,
                     *args,
                     **kwargs):
        if version == PRTVersion.V2:
            dialect = get_dialect(dialect, version)
            return _PRTDocumentV2(elements, dialect, *args, **kwargs)
        raise InvalidVersion(version)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def from_html(cls, string, version=PRTVersion.HIGHEST, *arg, **kwargs):
        if version == PRTVersion.V2:
            return _PRTDocumentV2.from_html(string, *arg, **kwargs)
        raise InvalidVersion(version)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def from_json(cls, string, version=PRTVersion.HIGHEST, *arg, **kwargs):
        if version == PRTVersion.V2:
            return _PRTDocumentV2.from_json(string, *arg, **kwargs)
        raise InvalidVersion(version)
