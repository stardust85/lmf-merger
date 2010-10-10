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
import language_coding as language_coding_module
import lexical_entry as lexical_entry_module
from lmf_tools import *

# detect, if it is an explanatory lexicon, or a translation lexicon

class Lexicon:
	"""
	Class for storing a LMF lexicon.
	"""

	def __init__(self, xmlnode, language_coding):
		#
		# parse language
		#
		lang = get_feat(xmlnode, 'lang')
		self.lang = language_coding_module.to_ISO_639_3(lang, language_coding)

		#
		# parse lexical entries
		#
		lex_entry_nodes = xmlnode.getElementsByTagName('LexicalEntry')
		self.lex_entries = dict()

		for node in lex_entry_nodes:
			lex_entry = lexical_entry_module.LexicalEntry(node)
			if lex_entry.pos not in self.lex_entries:
				self.lex_entries[lex_entry.pos] = dict()

			self.lex_entries[lex_entry.pos][lex_entry.lemma] = lex_entry


	def merge_with_lexicon(self, another_lexicon):
		"""Add content of another lexicon to me"""
		#
		# TODO check languate (should match)
		#

		#
		# merge lexical entries
		#

		# go thru parts of speech in other lexicon
		for pos in another_lexicon.lex_entries:
			# do I have this part of speech in my lexicon?
			if pos not in self.lex_entries:
				# no, I will add it all from another lexicon
				# (by linking - it is mutable :)
				self.lex_entries[pos] = another_lexicon.lex_entries
			else:
				# yes, we have to check each lexical entry
				for lemma in another_lexicon.lex_entries[pos]:
					if lemma in self.lex_entries[pos]:
						# we have to merge them
						self.lex_entries[pos][lemma].merge_with_lex_entry(another_lexicon.lex_entries[pos][lemma])
					else:
						# add it
						self.lex_entries[pos][lemma] = another_lexicon.lex_entries[pos][lemma]


	def build_elem(self, dom):
		lexicon_elem = dom.createElement('Lexicon')
		add_feat(dom, lexicon_elem, 'lang', self.lang)

		# add lexical entries
		for pos in self.lex_entries:
			for lemma in self.lex_entries[pos]:
				lexicon_elem.appendChild(self.lex_entries[pos][lemma].build_elem(dom))
		return lexicon_elem
