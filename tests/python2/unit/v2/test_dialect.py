# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.error      import PRTError
from prt.v2.dialect import (PRTDialect,
                            PRTDialectError,
                            NameMustBeOverriden)


#------------------------------------------------------------------------------#
class TestPRTDialect(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_error(self):
        self.assertTrue(issubclass(PRTDialectError, PRTError))
        self.assertTrue(issubclass(NameMustBeOverriden, PRTDialectError))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_default_properties(self):
        self.assertEqual(PRTDialect.NAME, None)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_default_methods(self):
        PRTDialect.validate_identifier(None)
        PRTDialect.validate_attribute(None, None, None)
        self.assertEqual(PRTDialect.identifier_to_html(None), 'div')
        self.assertEqual(PRTDialect.identifier_from_html(None), 0)
        self.assertEqual(
            PRTDialect.attribute_to_html(None, None, None), (None, None))
        self.assertEqual(
            PRTDialect.attribute_from_html(None, None, None), (None, None))
