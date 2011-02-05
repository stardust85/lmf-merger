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

from lmf_tools import *
from language_coding import *

class EquivalentSet:
    def __init__(self, xmlnode, global_info):
        self.equivalent_set = set()
        equiv_elems = get_child_elements(xmlnode, 'Equivalent')
        for equiv_elem in equiv_elems:
            lang = get_feat(equiv_elem, 'lang')
            lang is None:
                lang = 'missing'
            writtenform = get_feat(equiv_elem, 'writtenForm')
