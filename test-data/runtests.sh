#!/bin/bash

set -x
set -e

file1=*1.xml
file2=*2.xml

for dir in test*
do
  cd $dir
  if [ -f runtest.sh ]; then
    ./runtest.sh
  else
    ../../src/lmf_merger.py $file1 $file2 merged.xml
    diff -u merged.xml merged_correct.xml
  fi
  cd ..
done
