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
from lexicon import merge_types

SENSE_SIMILARITY_THRESHOLD = 0.80


def get_definitions(sense_node):
    definition_elements = get_child_elements(sense_node, 'Definition')
    definitions = set()

    for definition_el in definition_elements:
        definitions.add(get_feat(definition_el, 'text'))

    if len(definitions) > 1:
        self.my_print('Warning: more than one definition in one sense. '+
        'We will use only the first one')
    return definitions

def get_equivalent(sense_node):
    equiv_elements = get_child_elements(sense_node, 'Equivalent')
    equivs = set()

    for equiv_el in equiv_elements:
        equivs.add(get_feat(equiv_el, 'writtenForm'))
    return equivs


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
            self.definitions.add(definitions[0])

        # equivalent
        equivs = get_equivalents(sense_node)
        if equivs:
            self.equivalents.add(equivs[0])


    def __init__(self, lex_entry_node):
        self.definitions = set()
        sense_nodes = get_child_elements(lex_entry_node, 'Sense')

        for sense_node in sense_nodes:
            self.__insert_node_to_deflist(sense_node)
            self.__insert_node_to_equivlist(sense_node)


    def merge_with_senselist(self, senselist, merge_type):
        """
        Merges senses from first node to second.
        """
        if merge_type == merge_types.BY_DEFINITION:
            for other_definition in senselist.definition_list:
                has_similar_sense = False
                for my_definition in self.definition_list:
                    print my_definition, other_definition, compare_definitions(my_definition, other_definition)
                    if compare_definitions(my_definition, other_definition) > SENSE_SIMILARITY_THRESHOLD:
                        has_similar_sense = True
                if not has_similar_sense:
                    self.definitions.add(other_definition)
        elif merge_type == merge_types.BY_EQUIVALENT:
            self.equivalents |= senselist.equivalents


    def build_elem(self, dom):
        sense_elem_list = list()
        if merge_type == merge_types.BY_DEFINITION:
            for definition in self.definition_list:
                sense_elem = dom.createElement('Sense')
                definition_elem = dom.createElement('Definition')
                add_feat(dom, definition_elem, 'text', definition)
                sense_elem.appendChild(definition_elem)
                sense_elem_list.append(sense_elem)
        elif merge_type == merge_types.BY_EQUIVALENT:
            for equiv in self.equivalents:
                sense_elem = dom.createElement('Sense')
                equiv_elem = dom.createElement('Equivalent')
                add_feat(dom, equiv_elem, 'writtenForm', equiv)
                sense_elem.appendChild(equiv_elem)
                sense_elem_list.appen(sense_elem)

        return sense_elem_list
