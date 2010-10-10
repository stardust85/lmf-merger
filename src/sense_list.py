#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
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

from __future__ import division
from lmf_tools import *

SENSE_SIMILARITY_THRESHOLD = 0.80


def get_definitions(sense_node):
	definition_elements = get_child_elements(sense_node, 'Definition')
	definitions = list()

	for definition_el in definition_elements:
		definitions.append(get_feat(definition_el, 'text'))

	if len(definitions) > 1:
		self.my_print('Warning: more than one definition in one sense. '+
		'We will use only the first one')
	return definitions


def compare_definitions(definition1, definition2):
	"""
	Returns similarity ranks of two senses.
	1. TODO removes too frequent words (they don't contain the important things)
	2. counts how many words from first set is in the second and vice-versa

	"""
	words1 = get_words(definition1)
	words2 = get_words(definition2)

	common_words = set(words1) & set(words2)
	# TODO replace this stupid algorithm by something better from nltk
	return (len(common_words)) / ((len(words1) + len(words2))/2)



class SenseList:
	"""
	Class for storing a list of senses.
	Each sense will be represented by its definition, or list of senses.
	TODO: Implement nested sense lists.
	"""
	def __insert_node_to_deflist(self, sense_node):
		# does it have a definition, or list of senses?
		definitions = get_definitions(sense_node)
		if definitions:
			self.definition_list.append(definitions[0])


	def __init__(self, lex_entry_node):
		self.definition_list = list()
		sense_nodes = get_child_elements(lex_entry_node, 'Sense')

		for sense_node in sense_nodes:
			self.__insert_node_to_deflist(sense_node)


	def merge_with_senselist(self, senselist):
		"""
		Merges senses from first node to second.
		"""
		for other_definition in senselist.definition_list:
			has_similar_sense = False
			for my_definition in self.definition_list:
				print my_definition, other_definition, compare_definitions(my_definition, other_definition)
				if compare_definitions(my_definition, other_definition) > SENSE_SIMILARITY_THRESHOLD:
					has_similar_sense = True
			if not has_similar_sense:
				self.definition_list.append(other_definition)


	def build_elem(self, dom):
		sense_elem_list = list()

		for definition in self.definition_list:
			sense_elem = dom.createElement('Sense')
			definition_elem = dom.createElement('Definition')
			add_feat(dom, definition_elem, 'text', definition)
			sense_elem.appendChild(definition_elem)
			sense_elem_list.append(sense_elem)

		return sense_elem_list
