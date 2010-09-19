#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Lexicon.py
#
#       Copyright 2010 Michel Samia <m.samia@seznam.cz>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import xml.dom.minidom
import LanguageCoding
from LmfTools import *

class Lexicon:
	"""
	Class for storing a LMF lexicon.
	"""

	def __init__(self, xmlnode, language_coding):
		#
		# parse language
		#
		lang = get_feat(xmlnode, 'lang')
		self.lang = LanguageCoding.to_ISO_639_3(lang, language_coding)

	def merge_with_lexicon(self, another_lexicon):
		pass

	def build_elem(self, document):
		dom = document.createElement('Lexicon')
		return dom
