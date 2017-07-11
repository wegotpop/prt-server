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
        for i in range(0x17):
            PRTPOPDialect.validate_identifier(i)
        self.assertRaises(InvalidIdentifier,
                          PRTPOPDialect.validate_identifier,
                          0x18)

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
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x02), 'blockquote')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x03), 'code')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x04), 'div')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x05), 'h1')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x06), 'h2')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x07), 'h3')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x08), 'h4')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x09), 'h5')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x0A), 'h6')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x0B), 'h7')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x0C), 'i')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x0D), 'img')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x0E), 'li')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x0F), 'ol')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x10), 'p')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x11), 'pre')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x12), 's')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x13), 'span')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x14), 'sub')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x15), 'sup')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x16), 'u')
        self.assertEqual(PRTPOPDialect.identifier_to_html(0x17), 'ul')

        self.assertEqual(PRTPOPDialect.identifier_from_html('a'), 0x00)
        self.assertEqual(PRTPOPDialect.identifier_from_html('b'), 0x01)
        self.assertEqual(PRTPOPDialect.identifier_from_html('blockquote'), 0x02)
        self.assertEqual(PRTPOPDialect.identifier_from_html('code'), 0x03)
        self.assertEqual(PRTPOPDialect.identifier_from_html('div'), 0x04)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h1'), 0x05)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h2'), 0x06)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h3'), 0x07)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h4'), 0x08)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h5'), 0x09)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h6'), 0x0A)
        self.assertEqual(PRTPOPDialect.identifier_from_html('h7'), 0x0B)
        self.assertEqual(PRTPOPDialect.identifier_from_html('i'), 0x0C)
        self.assertEqual(PRTPOPDialect.identifier_from_html('img'), 0x0D)
        self.assertEqual(PRTPOPDialect.identifier_from_html('li'), 0x0E)
        self.assertEqual(PRTPOPDialect.identifier_from_html('ol'), 0x0F)
        self.assertEqual(PRTPOPDialect.identifier_from_html('p'), 0x10)
        self.assertEqual(PRTPOPDialect.identifier_from_html('pre'), 0x11)
        self.assertEqual(PRTPOPDialect.identifier_from_html('s'), 0x12)
        self.assertEqual(PRTPOPDialect.identifier_from_html('span'), 0x13)
        self.assertEqual(PRTPOPDialect.identifier_from_html('sub'), 0x14)
        self.assertEqual(PRTPOPDialect.identifier_from_html('sup'), 0x15)
        self.assertEqual(PRTPOPDialect.identifier_from_html('u'), 0x16)
        self.assertEqual(PRTPOPDialect.identifier_from_html('ul'), 0x17)
