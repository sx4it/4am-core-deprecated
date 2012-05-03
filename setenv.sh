#!/bin/bash 

ABSPATH=$(cd `dirname $BASH_SOURCE` && pwd)

export PYTHONPATH=${PYTHONPATH}:${ABSPATH}/lib
export PATH=${PATH}:${ABSPATH}/bin
