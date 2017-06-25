# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from unittest import TestCase

# Import from PRT modules
from prt.error import PRTError


#------------------------------------------------------------------------------#
class TestPRTError(TestCase):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_instance(self):
        self.assertTrue(issubclass(PRTError, Exception))
