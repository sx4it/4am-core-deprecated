#!/bin/bash 

ABSPATH=$(cd `dirname $BASH_SOURCE` && pwd)

export PYTHONPATH=${PYTHONPATH}:$ABSPATH
export PATH=${PATH}:${ABSPATH}
