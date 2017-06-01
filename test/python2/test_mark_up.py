# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from unittest import TestCase

from prt.v2.pop_dialect import PRTPOPDialect
from prt.v2.mark_up     import (PRTMarkUp,
                                InvalidElementsType,
                                InvalidElementType,
                                InvalidTagValue,
                                InvalidPropertyForTag)

PRTMarkUpPop = lambda e: PRTMarkUp(e, PRTPOPDialect)

class TestPRTMarkUp(TestCase):

    def test_invalid_elements(self):
        self.assertRaises(InvalidElementsType, PRTMarkUpPop(True).validate)
        self.assertRaises(InvalidElementsType, PRTMarkUpPop(False).validate)
        self.assertRaises(InvalidElementType, PRTMarkUpPop([()]).validate)
        self.assertRaises(InvalidElementType, PRTMarkUpPop([(0x00,)]).validate)
        self.assertRaises(InvalidElementType, PRTMarkUpPop([(0x00, None)]).validate)

    def test_invalid_tag(self):
        self.assertRaises(InvalidTagValue, PRTMarkUpPop([(-0xFF, None, None)]).validate)

    def test_invalid_props_to_html(self):
        self.assertRaises(InvalidPropertyForTag, PRTMarkUpPop([(0x00, '', None)]).validate)
        self.assertRaises(InvalidPropertyForTag, PRTMarkUpPop([(0x00, set(), None)]).validate)
        self.assertRaises(InvalidPropertyForTag, PRTMarkUpPop([(0x00, ['ab', 'cd'], None)]).validate)
        self.assertRaises(InvalidPropertyForTag,
                          PRTMarkUpPop([(0x01, {'onClick': 'p("clicked!")'}, None)]).validate)
        self.assertRaises(InvalidPropertyForTag,
                          PRTMarkUpPop([(0x01, {'href': '#'}, None)]).validate)
        self.assertRaises(InvalidPropertyForTag,
                          PRTMarkUpPop([(0x01, {'src': '#'}, None)]).validate)
        self.assertRaises(InvalidPropertyForTag,
                          PRTMarkUpPop([(0x0B, {'href': 'x'}, None)]).validate)

    def test_empty_elems_to_html(self):
        self.assertEqual(str(PRTMarkUpPop(None)), '')
        self.assertEqual(str(PRTMarkUpPop('')), '')
        self.assertEqual(str(PRTMarkUpPop([])), '')

    def test_single_string_to_html(self):
        self.assertEqual(str(PRTMarkUpPop('element')), 'element')

    def test_single_elems_no_children_no_props_to_html(self):
        self.assertEqual(str(PRTMarkUpPop([(0x01, None, None)])), '<b></b>')
        self.assertEqual(str(PRTMarkUpPop([(0x01, None, '')])), '<b></b>')
        self.assertEqual(str(PRTMarkUpPop([(0x01, None, [])])), '<b></b>')

    def test_nested_elems_single_child_no_props_to_html(self):
        self.assertEqual(str(PRTMarkUpPop([(0x0C, None, None)])), '<p></p>')
        self.assertEqual(str(PRTMarkUpPop(
            [(0x03, None,
                [(0x04, None,
                    [(0x05, None,
                        [(0x06, None,
                            [(0x07, None,
                                [(0x08, None,
                                    [(0x09, None, 'hello')])])])])])])])),
            '<h1><h2><h3><h4><h5><h6><h7>hello</h7></h6></h5></h4></h3></h2></h1>')

    def test_elem_with_special_html_no_props_to_html(self):
        self.assertEqual(str(PRTMarkUpPop([(0x0B, None, None)])), '<img>')

    def test_single_elems_no_children_no_props_to_html(self):
        self.assertEqual(str(PRTMarkUpPop([(0x01, {'id': 'x'}, None)])), '<b id="x"></b>')
        self.assertEqual(str(PRTMarkUpPop([(0x01, {'id': 'x', 'class': 'y'}, '')])),
                         '<b class="y" id="x"></b>')
        self.assertEqual(str(PRTMarkUpPop([(0x00, {'href': '#'}, [])])), '<a href="#"></a>')
        self.assertEqual(str(PRTMarkUpPop([(0x00, {'id': 'x', 'class': 'y', 'href': '#'}, [])])),
                         '<a class="y" href="#" id="x"></a>')
        self.assertEqual(str(PRTMarkUpPop([(0x0B, {'alt': 'x', 'src': 'y'}, [])])),
                         '<img alt="x" src="y">')
        self.assertEqual(str(PRTMarkUpPop([(0x0B, {'id': 'u', 'class': 'v', 'alt': 'x', 'src': 'y'}, [])])),
                        '<img alt="x" class="v" id="u" src="y">')

    def test_nested_elems_single_child_no_props_to_html(self):
        self.assertEqual(str(PRTMarkUpPop([(0x0C, None, None)])), '<p></p>')
        self.assertEqual(str(PRTMarkUpPop(
            [(0x03, {'id': '0x03'},
                [(0x04, {'id': '0x04'},
                    [(0x05, {'id': '0x05'},
                        [(0x06, {'id': '0x06'},
                            [(0x07, {'id': '0x07'},
                                [(0x08, {'id': '0x08'},
                                    [(0x09, {'id': '0x09'}, 'hello')])])])])])])])),
            ('<h1 id="0x03">'
                '<h2 id="0x04">'
                    '<h3 id="0x05">'
                        '<h4 id="0x06">'
                            '<h5 id="0x07">'
                                '<h6 id="0x08">'
                                    '<h7 id="0x09">hello</h7>'
                                '</h6>'
                            '</h5>'
                        '</h4>'
                    '</h3>'
                '</h2>'
            '</h1>'))
