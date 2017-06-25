# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from PRT modules
from prt.error import PRTError


#------------------------------------------------------------------------------#
class PRTDialectError(PRTError): pass
#------------------------------------------------------------------------------#
class NameMustBeOverriden(PRTDialectError):

    _MESSAGE = 'PRTDialect.NAME must be overriden by all subclasses'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        super(NameMustBeOverriden, self).__init__(self._MESSAGE)


#------------------------------------------------------------------------------#
class PRTDialect(object):

    NAME = None

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def validate_identifier(cls, identifier):
        pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def validate_attribute(cls, identifier, attribute_name, attribute_value):
        pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def identifier_to_html(cls, identifier):
        return 'div'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def identifier_from_html(cls, identifier):
        return 0

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def attribute_to_html(cls, identifier, attribute_name, attribute_value):
        return attribute_name, attribute_value

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def attribute_from_html(cls, identifier, attribute_name, attribute_value):
        return attribute_name, attribute_value
