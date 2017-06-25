# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.version import PRTVersion, InvalidVersion


#------------------------------------------------------------------------------#
class TestPRTVersion(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_numbered(self):
        self.assertEqual(PRTVersion.V1.value, '1.0')
        self.assertEqual(PRTVersion.V2.value, '2.0')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_aliased(self):
        self.assertEqual(PRTVersion.LOWEST, PRTVersion.V1)
        self.assertEqual(PRTVersion.HIGHEST, PRTVersion.V2)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_order(self):
        self.assertEqual(tuple(PRTVersion), (PRTVersion.V1, PRTVersion.V2))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_error(self):
        self.assertEqual(InvalidVersion().message,
                         'Expected one of PRTVersion.V1, PRTVersion.V2, '
                         'but got: None (type NoneType)')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_as_int_tuple(self):
        self.assertEqual(PRTVersion.V1.as_int_tuple(), (1, 0))
        self.assertEqual(PRTVersion.V2.as_int_tuple(), (2, 0))
