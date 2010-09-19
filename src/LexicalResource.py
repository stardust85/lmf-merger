#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       LexicalResource.py
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

from LmfTools import *
import Lexicon
import LanguageCoding

DEFAULT_DTD_VERSION = "16"
DEFAULT_LANGUAGE_CODING = "ISO 639-3"

class LexicalResourceError(Exception):
	"""Base class for exceptions in this module"""
	pass

class IncompatibleDTDError(LexicalResourceError):
	def __init__(self, my_version, other_version):
		self.my_version = my_version
		self.other_version = other_version

class LexicalResource:
	"""
	Class for manipulation with LMF lexical resources.
	"""

	def __init__(self, xmlnode):
		"""
		Reads information from LMF root node into python data structures.
		"""
		# read DTD version
		try:
			self.dtdVersion = xmlnode.attributes['dtdVersion'].value
		except KeyError:
			self.dtdVersion = None

		#
		# read global information
		#
		gi_node = get_child_elements(xmlnode, 'GlobalInformation')[0]
		self.global_info = get_feats(gi_node)

		# language coding
		language_coding = None
		if 'languageCoding' in self.global_info:
			language_coding = self.global_info['languageCoding']

		# read lexicons
		self.lexicons = dict()
		lexicon_nodes = get_child_elements(xmlnode, 'Lexicon')
		for node in lexicon_nodes:
			lexicon = Lexicon.Lexicon(node, language_coding)

			# is there already a lexicon with same lang?
			if(lexicon.lang in self.lexicons):
				self.lexicons[lexicon.lang].merge_with_lexicon(lexicon)
			else:
				self.lexicons[lexicon.lang] = lexicon


	def merge_with_LR(self, anotherLR):
		"""
		Adds to myself data from another lexical resource.
		"""

		#
		# check DTD version
		#
		if anotherLR.dtdVersion != self.dtdVersion:
			raise IncompatibleDTDError(self.dtdVersion, anotherLR.dtdVersion)

		#
		# merge global information
		#


		#
		# merge lexicons
		#
		for lang in anotherLR.lexicons:
			# do I have this language?
			if lang in self.lexicons:
				self.lexicons[lang].merge_with_lexicon(anotherLR.lexicons[lang])


	def update_DOM(self):
		domImplementation = xml.dom.minidom.getDOMImplementation()
		dtd = domImplementation.createDocumentType('LexicalResource', None, "DTD_LMF_REV_16.dtd")
		self.dom = domImplementation.createDocument(None, 'LexicalResource', dtd)

		# add dtd version
		self.dom.documentElement.setAttribute('dtdVersion', DEFAULT_DTD_VERSION)

		# add global information
		elem = self.dom.createElement('GlobalInformation')
		self.dom.documentElement.appendChild(elem)

		# add lexicons
		for lexicon in self.lexicons:
			self.dom.documentElement.appendChild(self.lexicons[lexicon].build_elem(self.dom))
