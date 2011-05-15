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
from language_coding import *
import collections

Equiv = collections.namedtuple('Equiv', 'lang, writtenForm')

class EquivalentSet:
    """
    Converts sense xml node to set of tuples (lang, equiv_written_form),
    and back. Allows merges and comparisons.
    """
    def __init__(self, xmlnode, global_info):
        self.equivalent_set = set()
        equiv_elems = get_child_elements(xmlnode, 'Equivalent')
        for equiv_elem in equiv_elems:
            lang = get_feat(equiv_elem, 'lang')
            lang = to_ISO_639_2T(lang, global_info.get('languageCoding'))
            writtenform = get_feat(equiv_elem, 'writtenForm')

            self.equivalent_set.add( Equiv(lang, writtenform) )

    def equals_to(self, another):
        """
        Equivalent sets (of the same lemma) are equal,
        iff atleast one translation is equal.
        """
        return bool(self.equivalent_set & another.equivalent_set)

    def merge_with_another(self, another):
        self.equivalent_set |= another.equivalent_set

    def build_elems(self, dom):
        elems = list()
        for equiv in self.equivalent_set:
            elem = dom.createElement('Equivalent')
            if not equiv.lang is None:
                add_feat(dom, elem, 'lang', equiv.lang)
            add_feat(dom, elem, 'writtenForm', equiv.writtenForm)
            elems.append(elem)

        return elems
