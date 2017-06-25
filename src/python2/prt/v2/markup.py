# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from standard modules
from cgi       import escape
from lxml.html import (Element,
                       tostring)

# Import from PRT modules
from prt.error import PRTError


#------------------------------------------------------------------------------#
class PRTMarkUpError(PRTError): pass
#------------------------------------------------------------------------------#
class InvalidElementsType(PRTMarkUpError): pass
#------------------------------------------------------------------------------#
class InvalidElementType(PRTMarkUpError): pass
#------------------------------------------------------------------------------#
class InvalidAttributesToIdentifier(PRTMarkUpError): pass
#------------------------------------------------------------------------------#
class InvalidAttributeToIdentifier(PRTMarkUpError): pass
#------------------------------------------------------------------------------#
# Used by dialects:
class InvalidIdentifier(PRTMarkUpError): pass


#------------------------------------------------------------------------------#
class PRTMarkUp(object):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, elements, dialect):
        # TODO: add sanitisation to elements, for example, if it is an empty
        #       string or an empty iterable, then make it None, etc.
        self._elements  = elements
        self._dialect   = dialect
        self._validated = False

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __nonzero__(self):
        return bool(self._elements)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __eq__(self, other):
        # TODO: Consider checking the dialects as well?
        return (isinstance(other, self.__class__) and
                self._elements == other._elements)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __ne__(self, other):
        return not self.__eq__(other)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def _append_element_to_etree(self, element, root):
        if element is None:
            return
        elif isinstance(element, unicode):
            element = escape(element, quote=True)
            try:
                root[-1].tail = element
            except IndexError:
                root.text = element
            return

        identifier, attributes, elements = element
        element = Element(self._dialect.identifier_to_html(identifier))
        if attributes is not None:
            for name, value in sorted(attributes.iteritems()):
                element.set(
                    *self._dialect.attribute_to_html(identifier, name, value))

        self._append_elements_to_etree(elements, element)
        root.append(element)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def _append_elements_to_etree(self, elements, root):
        if elements is None:
            return
        elif isinstance(elements, unicode):
            try:
                root[-1].tail = elements
            except IndexError:
                root.text = elements
            return

        for element in elements:
            self._append_element_to_etree(element, root)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def append_to_etree(self, root):
        try:
            self._validated or self.validate()
            self._append_elements_to_etree(self._elements, root)
        except PRTMarkUpError:
            element = Element('del')
            element.text = 'Invalid PRTMarkUp'
            root.append(element)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def to_html(self):
        if self._elements is None:
            return ''
        elif isinstance(self._elements, unicode):
            return escape(self._elements, quote=True)
        dummy_root = Element('dummy_root')
        self.append_to_etree(dummy_root)
        return ''.join(tostring(element) for element in dummy_root)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def _validate_attributes(self, identifier, attributes):
        if attributes is None:
            return

        try:
            for name, value in attributes.iteritems():
                if not isinstance(value, unicode):
                    raise InvalidAttributeToIdentifier(
                        'Expected a string as the attribute value, but got: '
                        '{0!r} (type {0.__class__.__name__})'.format(value))
                self._dialect.validate_attribute(identifier, name, value)
        except AttributeError:
            raise InvalidAttributesToIdentifier(
                'Expected a dict-like attributes object, but '
                'got: {0!r} (type {0.__class__.__name__})'.format(attributes))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def _validate_element(self, element):
        if (element is None or
            isinstance(element, unicode)):
                return

        try:
            identifier, attributes, elements = element
        except (TypeError, ValueError):
            raise InvalidElementType(
                'Expected an iterable of 3 items, '
                'but got: {0!r} (type {0.__class__.__name__})'.format(element))

        self._dialect.validate_identifier(identifier)
        self._validate_attributes(identifier, attributes)
        self._validate_elements(elements)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def _validate_elements(self, elements):
        if (elements is None or
            isinstance(elements, unicode)):
                return

        for element in elements:
            self._validate_element(element)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def validate(self):
        try:
            self._validate_elements(self._elements)
            self._validated = True
        except TypeError:
            raise InvalidElementsType(
                'Expected iterable, but got: {0!r} '
                '(type {0.__class__.__name__})'.format(self._elements))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def elements(self):
        if self._validated:
            # Require validation again, since this method is returning the
            # mutable elements which can be changed by the user
            # TODO: Probably it should be better to give the user a view-object
            self._validated = False
        else:
            self.validate()
        return self._elements

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    __str__ = to_html
