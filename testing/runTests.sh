#!/bin/bash

# echo -n "........................................................................"
# echo -n "................................................................. Passed"

echo -n "1/2  Testing: makeNovel FODT to FODT ............................ "
cd fodt
../../makeNovel.py -i novel.cnf -f FODT -d DEBUG -q -l novel-fodt.log
LOGDIFF=$(diff -q novel-fodt.log novel-fodt.log.reference)
LOGRES=$?
OUTDIFF=$(diff -q novel.fodt novel.fodt.reference)
OUTRES=$?
if [ $LOGRES -eq 0 ] && [ $OUTRES -eq 0 ]; then
    echo "Passed"
else
    echo "Failed"
    if [ $LOGRES -gt 0 ]; then
        echo "     Reason:  $LOGDIFF"
        diff novel-fodt.log novel-fodt.log.reference
    fi
    if [ $OUTRES -gt 0 ]; then
        echo "     Reason:  $OUTDIFF"
        diff novel.fodt novel.fodt.reference
    fi
fi
cd ..

echo -n "2/2  Testing: makeNovel TXT to FODT ............................. "
cd txt
../../makeNovel.py -i novel.cnf -f FODT -d DEBUG -q -l novel-fodt.log
LOGDIFF=$(diff -q novel-fodt.log novel-fodt.log.reference)
LOGRES=$?
OUTDIFF=$(diff -q novel.fodt novel.fodt.reference)
OUTRES=$?
if [ $LOGRES -eq 0 ] && [ $OUTRES -eq 0 ]; then
    echo "Passed"
else
    echo "Failed"
    if [ $LOGRES -gt 0 ]; then
        echo "     Reason:  $LOGDIFF"
        diff novel-fodt.log novel-fodt.log.reference
    fi
    if [ $OUTRES -gt 0 ]; then
        echo "     Reason:  $OUTDIFF"
        diff novel.fodt novel.fodt.reference
    fi
fi
cd ..
