#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       synset.py - class for representing synsets
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

import definition_set as definition_set_module
from lmf_tools import *

class Synset:
    """
    Synset is a class representing the set of shared meanings within
    the same language. Synset links synonyms forming a synonym set.
    A Synset instance can link senses of different Lexical Entry
    instances with the same part of speech.

    Example: In WordNet 2.1, the synset "12100067" groups together
    the meanings of oak and oak tree that are considered as synonymous.
    """

    def __init__(self, xmlnode, global_info):
        self.definitions = definition_set_module.DefinitionSet(xmlnode, global_info)
        self.old_id = xmlnode.get('id')
        self.new_id = None

    def equals_to(self, other):
        return self.definitions.equals_to(other.definitions)

    def __eq__(self, other):
        return equals_to(self, other)

    def __hash__(self):
        return self.definitions.__hash__()
        
    def compare_to(self, other):
        return self.definitions.compare_to(other.definitions)

    def build_elem(self, dom, lmf_id):
        elem = dom.createElement('Synset')
        elem.setAttribute('id', lmf_id)
        for definition_el in self.definitions.build_elems(dom):
            elem.appendChild(definition_el)

        return elem
