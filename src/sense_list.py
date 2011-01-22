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


from lmf_tools import *
from lexicon import merge_types
import definition as definition_module

SENSE_SIMILARITY_THRESHOLD = 0.80


def get_definitions(sense_node):
    definition_elements = get_child_elements(sense_node, 'Definition')
    definitions = list()

    for definition_el in definition_elements:
        definitions.append(definition_module.Definition(definition_el))

    if len(definitions) > 1:
        self.my_print('Warning: more than one definition in one sense. '+
        'We will use only the first one')
    return definitions

def get_equivalents(sense_node):
    equiv_elements = get_child_elements(sense_node, 'Equivalent')
    equivs = list()

    for equiv_el in equiv_elements:
        value = get_feat(equiv_el, 'writtenForm')
        if value == None:
            # TODO do this by LmfMerger.my_print and solve how to pass it here
            print 'Warning: no equivalent in ' + equiv_el.toxml()
        equivs.append(value)
    return equivs


class SenseList:
    """
    Class for storing a list of senses.
    Each sense will be represented by its definition, by list of equivalents,
    or by list of sub-senses.

    Actual implementation doens't support mixing both definitions and equivalents.

    TODO: Implement nested sense lists.
    """
    def __init__(self, lex_entry_node):
        """ fills itself by senses from a lexical entry"""
        self.definitions = set()
        self.equivalents = set()
        sense_nodes = get_child_elements(lex_entry_node, 'Sense')

        for sense_node in sense_nodes:
            self.__insert_node_to_deflist(sense_node)
            self.__insert_node_to_equivlist(sense_node)


    def __insert_node_to_deflist(self, sense_node):
        definitions = get_definitions(sense_node)
        if definitions:
            self.definitions.add(definitions[0])

    def __insert_node_to_equivlist(self, sense_node):
        # equivalent
        equivs = get_equivalents(sense_node)
        if equivs:
            self.equivalents.add(equivs[0])


    def merge_with_senselist(self, senselist, merge_type):
        """
        Merges senses from first node to second.
        """
        if merge_type == merge_types.BY_DEFINITION:
            for other_definition in senselist.definitions:
                has_similar_sense = False
                for my_definition in self.definitions:
                    print my_definition, other_definition, my_definition.compare_to(other_definition)
                    if my_definition.compare_to(other_definition) > SENSE_SIMILARITY_THRESHOLD:
                        has_similar_sense = True
                if not has_similar_sense:
                    self.definitions.add(other_definition)
        elif merge_type == merge_types.BY_EQUIVALENT:
            self.equivalents |= senselist.equivalents


    def build_elem(self, dom):
        sense_elem_list = list()
        if self.definitions:
            for definition in self.definitions:
                sense_elem = dom.createElement('Sense')
                definition_elem = definition.build_elem(dom)
                sense_elem.appendChild(definition_elem)
                sense_elem_list.append(sense_elem)
        elif self.equivalents:
            print self.equivalents
            for equiv in self.equivalents:
                sense_elem = dom.createElement('Sense')
                equiv_elem = dom.createElement('Equivalent')
                add_feat(dom, equiv_elem, 'writtenForm', equiv)
                sense_elem.appendChild(equiv_elem)
                sense_elem_list.append(sense_elem)

        return sense_elem_list
