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

    _VALID_IDENTIFIERS         = {0x00: 'a',
                                  0x01: 'b',
                                  0x02: 'code',
                                  0x03: 'h1',
                                  0x04: 'h2',
                                  0x05: 'h3',
                                  0x06: 'h4',
                                  0x07: 'h5',
                                  0x08: 'h6',
                                  0x09: 'h7',
                                  0x0A: 'i',
                                  0x0B: 'img',
                                  0x0C: 'p',
                                  0x0D: 'pre',
                                  0x0E: 's',
                                  0x0F: 'u'}
    _VALID_TAGS                = {v: k for k, v in
                                    _VALID_IDENTIFIERS.iteritems()}
    _VALID_GENERIC_ATTRIBUTES  = {'id', 'class'}
    _VALID_SPECIFIC_ATTRIBUTES = {0x00: {'href'},
                                  0x0B: {'alt', 'src'}}

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
