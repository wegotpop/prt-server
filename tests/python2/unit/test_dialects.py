# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.version    import (PRTVersion,
                            InvalidVersion)
from prt.v2.dialect import (PRTDialect,
                            NameMustBeOverriden)
from prt.dialects   import (register_dialect,
                            get_dialect,
                            InvalidDialectType,
                            InvalidDialectName,
                            InvalidDialectVersion)


#------------------------------------------------------------------------------#
class ValidDialect(PRTDialect):
    NAME = 'valid'

#------------------------------------------------------------------------------#
class InvalidDialect1(PRTDialect):
    pass

#------------------------------------------------------------------------------#
class InvalidDialect2(object):
    NAME = 'invalid'


#------------------------------------------------------------------------------#
class TestDialects(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_transaction(self):
        register_dialect(ValidDialect, PRTVersion.V2)
        dialect = get_dialect(ValidDialect.NAME, PRTVersion.V2)
        self.assertEqual(dialect, ValidDialect)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_register(self):
        self.assertRaises(InvalidVersion,
                          register_dialect, ValidDialect, 2.0)
        self.assertRaises(InvalidDialectType,
                          register_dialect, None, PRTVersion.V2)
        self.assertRaises(InvalidDialectType,
                          register_dialect, InvalidDialect2, PRTVersion.V2)
        self.assertRaises(NameMustBeOverriden,
                          register_dialect, InvalidDialect1, PRTVersion.V2)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_get(self):
        self.assertRaises(InvalidVersion,
                          get_dialect, ValidDialect.NAME, 2.0)
        self.assertRaises(InvalidDialectVersion,
                          get_dialect, None, PRTVersion.V1)
        register_dialect(ValidDialect, PRTVersion.V2)
        self.assertRaises(InvalidDialectName,
                          get_dialect, None, PRTVersion.V2)
