# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from PRT modules
from prt.v2.dialect import PRTDialect
from prt.v2.markup  import (InvalidIdentifier,
                            InvalidAttributeToIdentifier)


#------------------------------------------------------------------------------#
class PRTPOPDialect(PRTDialect):

    _VALID_IDENTIFIERS         = {0x00 : 'a',
                                  0x01 : 'b',
                                  0x02 : 'blockquote',
                                  0x03 : 'code',
                                  0x04 : 'div',
                                  0x05 : 'h1',
                                  0x06 : 'h2',
                                  0x07 : 'h3',
                                  0x08 : 'h4',
                                  0x09 : 'h5',
                                  0x0A : 'h6',
                                  0x0B : 'h7',
                                  0x0C : 'i',
                                  0x0D : 'img',
                                  0x0E : 'li',
                                  0x0F : 'ol',
                                  0x10 : 'p',
                                  0x11 : 'pre',
                                  0x12 : 's',
                                  0x13 : 'span',
                                  0x14 : 'sub',
                                  0x15 : 'sup',
                                  0x16 : 'u',
                                  0x17 : 'ul'}

    _VALID_TAGS                = {v: k for k, v in
                                    _VALID_IDENTIFIERS.iteritems()}
    _VALID_GENERIC_ATTRIBUTES  = {'id', 'class'}
    _VALID_SPECIFIC_ATTRIBUTES = {0x00: {'href', 'target'},
                                  0x0B: {'alt', 'src', 'title'}}

    NAME = 'pop'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def validate_identifier(cls, identifier):
        try:
            cls._VALID_IDENTIFIERS[identifier]
        except KeyError:
            raise InvalidIdentifier(
                'Expected one of {0!r}, but got: {1!r} (type '
                '{1.__class__.__name__})'.format(
                    tuple(cls._VALID_IDENTIFIERS.iterkeys()), identifier))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def validate_attribute(cls, identifier, attribute, _):
        try:
            valid_attributes = cls._VALID_SPECIFIC_ATTRIBUTES[identifier].copy()
        except KeyError:
            valid_attributes = set()

        valid_attributes |= cls._VALID_GENERIC_ATTRIBUTES

        if attribute not in valid_attributes:
            raise InvalidAttributeToIdentifier(
                'Expected to have one of {0!r}, but got {1!r} (type '
                '{1.__class__.__name__})'.format(valid_attributes, attribute))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def identifier_to_html(cls, identifier):
        return cls._VALID_IDENTIFIERS[identifier]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def identifier_from_html(cls, tag):
        return cls._VALID_TAGS[tag]
