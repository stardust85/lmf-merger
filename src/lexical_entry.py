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
import sense_list

class LexicalEntry:
    """
    Class for storing a lexical entry. i.e. sth. like one word.
    """

    def __init__(self, xmlnode, global_info):
        # set part of speech
        self.pos = get_part_of_speech(xmlnode)

        # set lemma written form
        lemma_elem = get_child_elements(xmlnode, 'Lemma')[0]
        self.lemma = get_feat(lemma_elem, 'writtenForm')

        # senses
        self.sense_list = sense_list.SenseList(xmlnode, global_info)

    def merge_with_lex_entry(self, lentry, merge_type):
        # merge senses
        self.sense_list.merge_with_senselist(lentry.sense_list, merge_type)

    def build_elem(self, dom):
        lentry_elem = dom.createElement('LexicalEntry')
        add_feat(dom, lentry_elem, 'partOfSpeech', self.pos)

        # add lemma
        lemma_elem = dom.createElement('Lemma')
        add_feat(dom, lemma_elem, 'writtenForm', self.lemma)
        lentry_elem.appendChild(lemma_elem)

        # add senses
        sense_elem_list = self.sense_list.build_elems(dom)

        for sense_elem in sense_elem_list:
            lentry_elem.appendChild(sense_elem)

        return lentry_elem
