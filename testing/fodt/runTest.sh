#!/bin/bash

../../makeNovel.py -i novel.cnf -d DEBUG -q -l novel.log
LOGDIFF=$(diff -q novel.log novel.log.reference)
LOGRES=$?
OUTDIFF=$(diff -q novel.fodt novel.fodt.reference)
OUTRES=$?
if [ $LOGRES -eq 0 ] && [ ]$OUTRES -eq 0 ]; then
    echo "Passed"
else
    echo "Failed"
    if [ $LOGRES -gt 0 ]; then
        echo "     Reason:  $LOGDIFF"
        diff novel.log novel.log.reference
    fi
    if [ $OUTRES -gt 0 ]; then
        echo "     Reason:  $OUTDIFF"
        diff novel.fodt novel.fodt.reference
    fi
fi
