# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)


# Import from standard modules
from unittest import TestCase

# Import from lxml modules
from lxml.html import tostring

# Import from PRT modules
from prt.error       import PRTError
from prt.version     import (PRTVersion,
                             InvalidVersion)
from prt.dialects    import (register_dialect,
                             InvalidDialectName)
from prt.v2.dialect  import PRTDialect
from prt.v2.document import (PRTDocument,
                             PRTDocumentError,
                             InvalidPRTDocument,
                             IncompatibleVersion)


#------------------------------------------------------------------------------#
class DummyDialect(PRTDialect):
    NAME = 'dummy'


#------------------------------------------------------------------------------#
class TestPRTDocument(TestCase):

    def setUp(self):
        register_dialect(DummyDialect, PRTVersion.V2)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_error(self):
        self.assertTrue(issubclass(PRTDocumentError, PRTError))
        self.assertTrue(issubclass(InvalidPRTDocument, PRTDocumentError))
        self.assertTrue(issubclass(IncompatibleVersion, PRTDocumentError))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_document(self):
        PRTDocument(None)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_bool(self):
        self.assertFalse(PRTDocument(None))
        self.assertTrue(PRTDocument('None'))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_equality(self):
        self.assertEqual(PRTDocument(None), PRTDocument(None))
        self.assertNotEqual(PRTDocument(None), PRTDocument('None'))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_from_html(self):
        self.assertEqual(
            PRTDocument.from_html(
                '<PRTDocument version="2.0" dialect="dummy"/>'),
            PRTDocument([], 'dummy'))
        self.assertEqual(
            PRTDocument.from_html(
                '<PRTDocument version="2.0" dialect="dummy">'
                    'text'
                '</PRTDocument>'),
            PRTDocument(['text'], 'dummy'))
        self.assertEqual(
            PRTDocument.from_html(
                '<PRTDocument version="2.0" dialect="dummy">'
                    '<div>text</div>'
                '</PRTDocument>'),
            PRTDocument([(0, None, 'text')], 'dummy'))
        self.assertEqual(
            PRTDocument.from_html(
                '<PRTDocument version="2.0" dialect="dummy">'
                    '<div></div>'
                '</PRTDocument>'),
            PRTDocument([(0, None, None)], 'dummy'))
        self.assertEqual(
            PRTDocument.from_html(
                '<PRTDocument version="2.0" dialect="dummy">'
                    '<div>'
                        '<div>text</div>'
                    '</div>'
                '</PRTDocument>'),
            PRTDocument([(0, None, [(0, None, 'text')])], 'dummy'))
        self.assertEqual(
            PRTDocument.from_html(
                '<PRTDocument version="2.0" dialect="dummy">'
                    '<div>'
                        '<div>text</div>'
                        'text2'
                    '</div>'
                '</PRTDocument>'),
            PRTDocument([(0, None, [(0, None, 'text'), 'text2'])],
                        'dummy'))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_from_html(self):
        self.assertRaises(InvalidPRTDocument, PRTDocument.from_html, '')
        self.assertRaises(InvalidPRTDocument, PRTDocument.from_html, '<br/>')
        self.assertRaises(IncompatibleVersion,
                          PRTDocument.from_html,
                          '<PRTDocument/>')
        self.assertRaises(IncompatibleVersion,
                          PRTDocument.from_html,
                          '<PRTDocument version="1.0"/>')
        self.assertRaises(InvalidDialectName,
                          PRTDocument.from_html,
                          '<PRTDocument version="2.0"/>')
        self.assertRaises(InvalidDialectName,
                          PRTDocument.from_html,
                          '<PRTDocument version="2.0" dialect="hello"/>')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_from_json(self):
        self.assertEqual(
            PRTDocument.from_json(
                '{'
                    '"type":"PRTDocument",'
                    '"version":"2.0",'
                    '"dialect":"dummy",'
                    '"elements":null'
                '}'),
            PRTDocument(None, DummyDialect))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_from_json(self):
        self.assertRaises(InvalidPRTDocument, PRTDocument.from_json, '')
        self.assertRaises(InvalidPRTDocument, PRTDocument.from_json, '{}')
        self.assertRaises(IncompatibleVersion,
                          PRTDocument.from_json,
                          '{"type":"PRTDocument"}')
        self.assertRaises(IncompatibleVersion,
                          PRTDocument.from_json,
                          '{"type":"PRTDocument","version":"1.0"}')
        self.assertRaises(InvalidDialectName,
                          PRTDocument.from_json,
                          '{"type":"PRTDocument","version":"2.0"}')
        self.assertRaises(InvalidDialectName,
                          PRTDocument.from_json,
                          '{'
                            '"type":"PRTDocument",'
                            '"version":"2.0",'
                            '"dialect":"hello"'
                          '}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_to_html(self):
        self.assertEqual(PRTDocument(None).to_html(),
                         '<PRTDocument version="2.0"></PRTDocument>')
        self.assertEqual(PRTDocument('text').to_html(),
                         '<PRTDocument version="2.0">'
                            'text'
                        '</PRTDocument>')
        self.assertEqual(PRTDocument([(0, None, 'text')], DummyDialect).to_html(),
                         '<PRTDocument version="2.0" dialect="dummy">'
                            '<div>'
                                'text'
                            '</div>'
                        '</PRTDocument>')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_to_json(self):
        self.assertEqual(PRTDocument(None).to_json(),
                         '{'
                             '"type":"PRTDocument",'
                             '"version":"2.0",'
                             '"elements":null'
                         '}')
        self.assertEqual(PRTDocument('text').to_json(),
                         '{'
                             '"type":"PRTDocument",'
                             '"version":"2.0",'
                             '"elements":"text"'
                         '}')
        self.assertEqual(PRTDocument([(0, None, 'text')], DummyDialect).to_json(),
                         '{'
                             '"type":"PRTDocument",'
                             '"version":"2.0",'
                             '"dialect":"dummy",'
                             '"elements":[[0,null,"text"]]'
                         '}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_alias(self):
        self.assertEqual(PRTDocument(None).to_html(), repr(PRTDocument(None)))
        self.assertEqual(PRTDocument(None).to_json(), str(PRTDocument(None)))
