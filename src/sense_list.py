#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       $$
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
import sense as sense_module
import equivalent_set as equivalent_set_module

SENSE_SIMILARITY_THRESHOLD = 0.80


class SenseList:
    """
    Class for storing a list of senses.
    Each sense will be represented by its definition, by list of equivalents,
    or by list of sub-senses.

    Actual implementation doens't support mixing both definitions and equivalents.

    TODO: Implement nested sense lists.
    """
    def __init__(self, lex_entry_node, global_info, lexicon):
        """ fills itself by senses from a lexical entry"""
        self.senses = set()

        sense_nodes = get_child_elements(lex_entry_node, 'Sense')

        for sense_node in sense_nodes:
            self.senses.add(sense_module.Sense(sense_node, global_info, lexicon))


    def merge_with_senselist(self, other_list, merge_type):
        """
        Merges senses from first node to second.
        """
        if merge_type == merge_types.BY_DEFINITION:
            for other_sense in other_list.senses:
                has_similar_sense = False
                for my_sense in self.senses:
                    if my_sense.compare_to(other_sense, merge_type) > SENSE_SIMILARITY_THRESHOLD:
                        has_similar_sense = True
                if not has_similar_sense:
                    self.senses.add(other_sense)

        elif merge_type == merge_types.BY_EQUIVALENT:
            for other_sense in other_list.senses:
                has_similar_sense = False
                for my_sense in self.senses:
                    if my_sense.equals_to(other_sense, merge_type):
                        my_sense.merge_with_sense(other_sense)
                        has_similar_sense = True
                if not has_similar_sense:
                    self.senses.add(other_sense)


    def build_elems(self, dom):
        sense_elem_list = list()
        for sense in self.senses:
            sense_elem_list.append(sense.build_elem(dom))

        return sense_elem_list
