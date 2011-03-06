#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       $$
#
#       Copyright 2011 Michel Samia <m.samia@seznam.cz>
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
import definition_set as definition_set_module
import equivalent_set as equivalent_set_module

class Sense:
    def __init__(self, xmlnode, global_info, lexicon):
        #
        # synset ID
        #
        if xmlnode.hasAttribute('synset'):
            self.synset_id = xmlnode.getAttribute('synset')
            self.synset = lexicon.synsets[self.synset_id]
        else:
            self.synset_id = None
            self.synset = None

        #
        # definitions
        #
        if self.synset is None:
            self.definitions = definition_set_module.DefinitionSet(xmlnode, global_info)
        else:
            self.definitions = self.synset.definitions

        #
        # equivalents - mapping each lang to its written form
        #
        self.equivalents = equivalent_set_module.EquivalentSet(xmlnode, global_info)

    def compare_to(self, other, compare_type):
        """ how much are the senses equal """
        if compare_type == merge_types.BY_DEFINITION:
            return self.definitions.compare_to(other.definitions)

    def equals_to(self, other, compare_type):
        """only for equiv"""
        if compare_type == merge_types.BY_EQUIVALENT:
            return self.equivalents.equals_to(other.equivalents)
        elif compare_type == merge_types.BY_DEFINITION:
            return self.definitions.equals_to(other.definitions)

    def merge_with_sense(self, other):
        self.equivalents.merge_with_another(other.equivalents)

    def build_elem(self, dom):
        print 'sense build', self
        sense_elem = dom.createElement('Sense')

        # add synset id
        if not self.synset_id is None:
            sense_elem.setAttribute('synset', self.synset_id)

        # add definitions
        if self.synset is None:
            for definition_el in self.definitions.build_elems(dom):
                sense_elem.appendChild(definition_el)

        # add equivalents
        equiv_elems = self.equivalents.build_elems(dom)
        for equiv_elem in equiv_elems:
            sense_elem.appendChild(equiv_elem)

        return sense_elem
