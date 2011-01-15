#!/bin/bash

file1=*1.xml
file2=*2.xml

for dir in test*
do
  ../src/lmf_merger.py $file1 $fiel2 merged.xml
  diff merged.xml merged_correct.xml
done
