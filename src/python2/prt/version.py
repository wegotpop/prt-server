# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from enum34 modules
from enum import Enum

# Import from PRT modules
from prt.error import PRTError


#------------------------------------------------------------------------------#
class PRTVersionError(PRTError): pass
#------------------------------------------------------------------------------#
class InvalidVersion(PRTVersionError):

    _MESSAGE = ('Expected one of {0}, but got: '
                '{1!r} (type {1.__class__.__name__})')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, version=None):
        super(InvalidVersion, self).__init__(
            self._MESSAGE.format(
                ', '.join('PRTVersion.{}'.format(v.name) for v in PRTVersion),
                version))


#------------------------------------------------------------------------------#
class PRTVersion(Enum):
    # TODO: py3: Remove the __order__ string
    __order__ = 'V1 V2'

    V1 = LOWEST  = '1.0'
    V2 = HIGHEST = '2.0'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def as_int_tuple(self):
        return tuple(map(int, self.value.split('.')))
