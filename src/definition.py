#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
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


from __future__ import division
from lmf_tools import *

DEF_SIMILARITY_THRESHOLD = 0.80



class Definition:
    def __init__(self, xmlnode):
        self.text = get_feat(xmlnode, 'text')

    def compare_to(self, other):
        """
        Returns similarity ranks of two senses.
        1. TODO removes too frequent words (they don't contain the important things)
        2. counts how many words from first set is in the second and vice-versa

        """
        words1 = get_words(self.text)
        words2 = get_words(other.text)

        common_words = set(words1) & set(words2)
        # TODO replace this stupid algorithm by something better from nltk
        return (len(common_words)) / ((len(words1) + len(words2))/2)

    def equals_to(self, other):
        return self.text == other.text

    def __eq__(self, other):
        return self.equals_to(other)

    def __hash__(self):
        return self.text

    def build_elem(self, dom):
        def_elem = dom.createElement('Definition')
        add_feat(dom, def_elem, 'text', self.text)
        return def_elem


