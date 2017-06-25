# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from lxml modules
from lxml.html import (Element,
                       tostring)

# Import from PRT modules
from prt.error      import PRTError
from prt.v2.dialect import PRTDialect
from prt.v2.markup  import (PRTMarkUp,
                            PRTMarkUpError,
                            InvalidIdentifier,
                            InvalidElementsType,
                            InvalidElementType,
                            InvalidAttributesToIdentifier,
                            InvalidAttributeToIdentifier)


#------------------------------------------------------------------------------#
class TestPRTMarkUp(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_error(self):
        self.assertTrue(issubclass(PRTMarkUpError, PRTError))
        self.assertTrue(issubclass(InvalidIdentifier, PRTMarkUpError))
        self.assertTrue(issubclass(InvalidElementsType, PRTMarkUpError))
        self.assertTrue(issubclass(InvalidElementType, PRTMarkUpError))
        self.assertTrue(issubclass(InvalidAttributesToIdentifier,
                                   PRTMarkUpError))
        self.assertTrue(issubclass(InvalidAttributeToIdentifier,
                                   PRTMarkUpError))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_bool(self):
        self.assertFalse(PRTMarkUp(None, None))
        self.assertTrue(PRTMarkUp('None', None))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_equality(self):
        class DummyMarkUp(object):
            _elements = None
        self.assertEqual(PRTMarkUp(None, None), PRTMarkUp(None, None))
        self.assertEqual(PRTMarkUp([], None), PRTMarkUp([], None))
        self.assertNotEqual(PRTMarkUp(None, None), PRTMarkUp([], None))
        self.assertNotEqual(PRTMarkUp(None, None), DummyMarkUp())

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_append_to_etree(self):
        root = Element('test_root')
        PRTMarkUp(None, None).append_to_etree(root)
        self.assertEqual(tostring(root), '<test_root></test_root>')

        root = Element('test_root')
        PRTMarkUp('text', None).append_to_etree(root)
        self.assertEqual(tostring(root), '<test_root>text</test_root>')

        root = Element('test_root')
        PRTMarkUp([None], PRTDialect).append_to_etree(root)
        self.assertEqual(tostring(root), '<test_root></test_root>')

        root = Element('test_root')
        PRTMarkUp(['text'], PRTDialect).append_to_etree(root)
        self.assertEqual(tostring(root), '<test_root>text</test_root>')

        root = Element('test_root')
        PRTMarkUp([[0, None, 'text']], PRTDialect).append_to_etree(root)
        self.assertEqual(tostring(root),
                         '<test_root><div>text</div></test_root>')

        root = Element('test_root')
        PRTMarkUp([[0, {'id': 'this'}, 'text']],
                  PRTDialect).append_to_etree(root)
        self.assertEqual(tostring(root),
                         '<test_root><div id="this">text</div></test_root>')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_append_to_etree(self):
        root = Element('test_root')
        PRTMarkUp(True, None).append_to_etree(root)
        self.assertEqual(tostring(root),
                         '<test_root><del>Invalid PRTMarkUp</del></test_root>')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_to_html(self):
        self.assertEqual(PRTMarkUp(None, PRTDialect).to_html(), '')
        self.assertEqual(PRTMarkUp('<div/>', PRTDialect).to_html(),
                         '&lt;div/&gt;')
        self.assertEqual(PRTMarkUp([None], PRTDialect).to_html(), '')
        self.assertEqual(PRTMarkUp('text', PRTDialect).to_html(), 'text')
        self.assertEqual(PRTMarkUp([(0, None, 'text')], PRTDialect).to_html(),
                                   '<div>text</div>')
        self.assertEqual(PRTMarkUp([(0, {'id': 'this'}, '<div/>')],
                                   PRTDialect).to_html(),
                         '<div id="this">&lt;div/&gt;</div>')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_validate(self):
        PRTMarkUp(None, None).validate()
        PRTMarkUp('text', None).validate()
        self.assertRaises(InvalidElementsType, PRTMarkUp(True, None).validate)
        self.assertRaises(InvalidElementType,
                          PRTMarkUp([(0, None)], None).validate)
        self.assertRaises(InvalidElementType,
                          PRTMarkUp([(0, None, None, None)], None).validate)
        self.assertRaises(InvalidAttributesToIdentifier,
                          PRTMarkUp([(0, True, None)], PRTDialect).validate)
        self.assertRaises(InvalidAttributeToIdentifier,
                          PRTMarkUp([(0, {'id': 0}, None)],
                                    PRTDialect).validate)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_elements(self):
        m = PRTMarkUp(None, None)
        # Validate and get elements
        self.assertEqual(m.elements(), None)
        # Validate again and get elements
        self.assertEqual(m.elements(), None)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_alias(self):
        self.assertEqual(PRTMarkUp(None, None).to_html(),
                         str(PRTMarkUp(None, None)))
