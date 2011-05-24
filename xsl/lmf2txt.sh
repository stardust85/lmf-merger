#!/bin/bash

xsltproc lmf2html.xsl $1 | html2text | less
