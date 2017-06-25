#!/bin/bash

COVERAGE_2_BINARY='';
COVERAGE_3_BINARY='';

# If "naked" python is  python2, then it is very likely that coverage2 is also "naked"
if [ "$(python -c 'from sys import stdout,version_info;stdout.write(str(version_info.major))')" = '2' ];
then
    COVERAGE_2_BINARY=coverage;
else
    COVERAGE_2_BINARY=coverage2;
fi;

# If "naked" python is python3, then it is very likely that coverage3 is also "naked"
if [ "$(python -c 'from sys import stdout,version_info;stdout.write(str(version_info.major))')" = '3' ];
then
    COVERAGE_3_BINARY=coverage;
else
    COVERAGE_3_BINARY=coverage3;
fi;

#
MAIN_ERROR_CODE=0;

check_error()
{
    if [ "$1" -ne 0 ];
    then
        MAIN_ERROR_CODE=1;
    fi;
}

# Run python 2 tests
PYTHONPATH="$PYTHONPATH:src/python2"                                           \
           $COVERAGE_2_BINARY run                                              \
           --source=src/python2/prt                                            \
           --module unittest discover tests/python2 --verbose;
check_error $?;

$COVERAGE_2_BINARY report --fail-under=100 --show-missing;
check_error $?;

# TODO: Run python 3 tests

exit $MAIN_ERROR_CODE;
