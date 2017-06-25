# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.document import PRTDocument
from prt.version  import PRTVersion


#------------------------------------------------------------------------------#
class TestPRTPOPDialectUsage(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_using_via_prtdocument(self):
        self.assertEqual(
            PRTDocument(None, version=PRTVersion.V2, dialect='pop').to_json(),
            '{'
                '"type":"PRTDocument",'
                '"version":"2.0",'
                '"dialect":"pop",'
                '"elements":null'
            '}')
