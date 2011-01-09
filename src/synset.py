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

import definition as definition_module
impor lmf_tools

class Synset:
    """
    Synset is a class representing the set of shared meanings within
    the same language. Synset links synonyms forming a synonym set.
    A Synset instance can link senses of different Lexical Entry
    instances with the same part of speech.

    Example: In WordNet 2.1, the synset "12100067" groups together
    the meanings of oak and oak tree that are considered as synonymous.
    """

    def __init__(self, xmlnode):
        def_elem = get_child_elements(xmlnode, 'Definition')[0]
        self.definition = definition_module.Definition(def_elem)

    def build_elem(self, dom, lmf_id):
        elem = dom.createElement('Synset')
        add_feat(dom, lexicon_elem, 'id', lmf_id)
        def_elem = self.definition.build_elem(dom)
        elem.appendChild(self.definition.build_elem())
