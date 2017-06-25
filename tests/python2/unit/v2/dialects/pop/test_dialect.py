# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.v2.markup               import (InvalidIdentifier,
                                         InvalidAttributeToIdentifier)
from prt.v2.dialects.pop.dialect import PRTPOPDialect


#------------------------------------------------------------------------------#
class TestPRTPOPDialect(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_identifier_validation(self):
        for i in range(0x0F):
            PRTPOPDialect.validate_identifier(i)
        self.assertRaises(InvalidIdentifier,
                          PRTPOPDialect.validate_identifier,
                          0x10)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_attribute_validation(self):
        for i in range(0x0F):
            PRTPOPDialect.validate_attribute(i, 'id', None)
            PRTPOPDialect.validate_attribute(i, 'class', None)

        PRTPOPDialect.validate_attribute(0x00, 'href', None)
        PRTPOPDialect.validate_attribute(0x0B, 'alt', None)
        PRTPOPDialect.validate_attribute(0x0B, 'src', None)

        self.assertRaises(InvalidAttributeToIdentifier,
                          PRTPOPDialect.validate_attribute,
                          0x01, 'href', None)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_identifier_conversion(self):
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x00), 'a')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x01), 'b')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x02), 'code')

        self.assertEqual(PRTPOPDialect.identifier_from_html('a'), 0x00)
        self.assertEqual(PRTPOPDialect.identifier_from_html('b'), 0x01)
        self.assertEqual(PRTPOPDialect.identifier_from_html('code'), 0x02)
