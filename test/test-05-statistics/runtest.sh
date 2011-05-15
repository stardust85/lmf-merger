#!/bin/bash

set -x
set -e

pwd
../../src/lmf_merger.py -s *xml* > stat.result

diff stat.result stat.result.correct
