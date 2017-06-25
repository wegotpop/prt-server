# -*- coding: utf-8 -*-
# Import compatibility features
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

# Import from PRT modules
from prt.error      import PRTError
from prt.version    import PRTVersion, InvalidVersion
from prt.v2.dialect import (PRTDialect          as _PRTDialectV2,
                            NameMustBeOverriden as _NameMustBeOverridenV2)

# TODO: There should be no built-in dialect!
from prt.v2.dialects.pop.dialect import PRTPOPDialect as PRTPOPDialectV2


#------------------------------------------------------------------------------#
class PRTDialectsError(PRTError): pass
#------------------------------------------------------------------------------#
class InvalidDialectType(PRTDialectsError): pass
#------------------------------------------------------------------------------#
class InvalidDialectName(PRTDialectsError): pass
#------------------------------------------------------------------------------#
class InvalidDialectVersion(PRTDialectsError): pass


#------------------------------------------------------------------------------#
# Module-level private constant
_DIALECTS = {}


#------------------------------------------------------------------------------#
def register_dialect(dialect, version):
    # Validate arguments
    if not isinstance(version, PRTVersion):
        raise InvalidVersion(version)
    try:
        if not issubclass(dialect, _PRTDialectV2):
            raise TypeError
    except TypeError:
        raise InvalidDialectType(
            'Expected a subclass of prt.v2.dialect.PRTDialect, but got: '
            '{0!r} (type {0.__class__.__name__})'.format(dialect))
    if dialect.NAME is None:
        raise _NameMustBeOverridenV2()
    # Store dialect
    _DIALECTS.setdefault(version, {})[dialect.NAME] = dialect


#------------------------------------------------------------------------------#
def get_dialect(name, version):
    # Validate arguments
    if not isinstance(version, PRTVersion):
        raise InvalidVersion(version)
    # Get dict referred by version
    try:
        dialects = _DIALECTS[version]
    except KeyError:
        raise InvalidDialectVersion(
            'No dialect registered with this version: {}'.format(version))
    # Get dialect referred by name
    try:
        return dialects[name]
    except KeyError:
        raise InvalidDialectName(
            'No dialect registered with this name and '
            'version: {} {}'.format(name, version))


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
register_dialect(PRTPOPDialectV2, PRTVersion.V2)
