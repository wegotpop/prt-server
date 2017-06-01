# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from enum import Enum


class PRTVersion(Enum):
    # TODO: py3: Remove the __order__ string
    __order__ = 'V1 V2'

    V2 = HIGHEST = '2.0'
    V1 = LOWEST  = '1.0'
