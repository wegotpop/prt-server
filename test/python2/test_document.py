# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from unittest import TestCase

from prt.document       import (PRTDocument,
                                InvalidVersion)
from prt.v2.pop_dialect import PRTPOPDialect
from prt.v2.document    import PRTDocument as PRTDocumentV2

PRTDocumentPop = lambda e: PRTDocument(e, dialect=PRTPOPDialect)

DOCUMENT_FMT = '<PRTDocument version="2.0" dialect="pop">{}</PRTDocument>'

class TestPRTDocument(TestCase):

    def test_empty_to_html(self):
        self.assertEqual(PRTDocumentPop([]).to_html(), DOCUMENT_FMT.format(''))
        self.assertEqual(PRTDocumentPop(None).to_html(), DOCUMENT_FMT.format(''))
        self.assertEqual(PRTDocumentPop('').to_html(), DOCUMENT_FMT.format(''))

    def test_valid_to_html(self):
        self.assertEqual(PRTDocumentPop('text').to_html(), DOCUMENT_FMT.format('text'))
        self.assertEqual(PRTDocumentPop([(0x00, {'href': '#'}, 'click')]).to_html(),
                         DOCUMENT_FMT.format('<a href="#">click</a>'))
        self.assertEqual(PRTDocumentPop([(0x00, {'href': '#'}, [(0x01, None, 'text')])]).to_html(),
                         DOCUMENT_FMT.format('<a href="#"><b>text</b></a>'))

    def test_version(self):
        self.assertRaises(InvalidVersion, PRTDocument, None, version=2)
        self.assertEqual(PRTDocumentPop(None), PRTDocumentV2(None, dialect=PRTPOPDialect))

    def test_bool(self):
        self.assertFalse(bool(PRTDocumentPop(None)))
        self.assertFalse(bool(PRTDocumentPop('')))
        self.assertFalse(bool(PRTDocumentPop([])))

        self.assertTrue(bool(PRTDocumentPop('text')))
        self.assertTrue(bool(PRTDocumentPop([(0x00, None, None)])))

    def test_from_html(self):
        html = DOCUMENT_FMT.format('<p><i class="x"><b id="y">hello</b></i></p>')
        self.assertEqual(html, PRTDocument.from_html(html, dialect=PRTPOPDialect).to_html())

    def test_from_json(self):
        json = ('{"type":"PRTDocument",'
                '"version":"2.0",'
                '"dialect":"pop",'
                '"elements":[[12,null,[[10,{"class":"x"},[[2,{"id":"y"},"hello"]]]]]]}')
        self.assertEqual(json, PRTDocument.from_json(json, dialect=PRTPOPDialect).to_json())
