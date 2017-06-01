#!/bin/bash

PYTHON_2_BINARY='';
PYTHON_3_BINARY='';

# Set python 2 binary
if [ "$(python -c 'from sys import stdout,version_info;stdout.write(str(version_info.major))')" = '2' ];
then
    PYTHON_2_BINARY=python;
else
    PYTHON_2_BINARY=python2;
fi;

# Set python 3 binary
if [ "$(python -c 'from sys import stdout,version_info;stdout.write(str(version_info.major))')" = '3' ];
then
    PYTHON_3_BINARY=python;
else
    PYTHON_3_BINARY=python3;
fi;

# Run python 2 tests
PYTHONPATH="$PYTHONPATH:src/python2" $PYTHON_2_BINARY -m unittest discover test/python2 --verbose;

# Run python 3 tests
# PYTHONPATH="$PYTHONPATH:src/python3" $PYTHON_3_BINARY -m unittest discover test/python3 --verbose;
