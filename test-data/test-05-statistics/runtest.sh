#!/bin/bash

set -x
set -e

../../src/lmf-merger.py -s *xml > stat.result

diff stat.result stat.result.correct
