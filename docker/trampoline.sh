#!/bin/sh
CWPROOT=/usr/local/cwp
torun=$CWPROOT/bin/`basename $0`
CWPROOT=$CWPROOT exec $torun $@
