# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.error          import PRTError
from prt.version        import (PRTVersion,
                                InvalidVersion)
from prt.document       import PRTDocument
from prt.dialects       import register_dialect
from prt.v2.dialect     import PRTDialect
from prt.v2.document    import PRTDocument as PRTDocumentV2


#------------------------------------------------------------------------------#
class TestDialect(PRTDialect):
    NAME = 'test'


#------------------------------------------------------------------------------#
class TestPRTDocument(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def setUp(self):
        register_dialect(TestDialect, PRTVersion.V2)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_empty_valid_document(self):
        PRTDocument(None, version=PRTVersion.V2, dialect='test')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_empty_invalid_document(self):
        self.assertRaises(InvalidVersion,
                          PRTDocument,
                          elements=None,
                          dialect='test',
                          version=2.0)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_simple_valid_document_from_html(self):
        PRTDocument.from_html('<PRTDocument version="2.0" dialect="test"/>')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_simple_invalid_document_from_html(self):
        self.assertRaises(InvalidVersion,
                          PRTDocument.from_html,
                          string='',
                          version=2.0)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_simple_valid_document_from_json(self):
        PRTDocument.from_json(
            '{'
                '"type":"PRTDocument",'
                '"version":"2.0",'
                '"dialect":"test",'
                '"elements":null'
            '}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_simple_invalid_document_from_json(self):
        self.assertRaises(InvalidVersion,
                          PRTDocument.from_json,
                          string='',
                          version=2.0)
