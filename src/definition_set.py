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
import definition as definition_module

class DefinitionSet:
    def __init__(self, parentnode, global_info):
        self.definitions = list()
        definition_elements = get_child_elements(parentnode, 'Definition')

        for definition_el in definition_elements:
            self.definitions.append(definition_module.Definition(definition_el, global_info))

    def compare_to(self, other):
        """TODO counts average of max similarities"""
        return self.definitions[0].compare_to(other.definitions[0])

    def equals_to(self, other):
        for other_def in other.definitions:
            for my_def in self.definitions:
                if other_def == my_def:
                    return True
        return False

    def build_elems(self, dom):
        elems = list()
        for definition in self.definitions:
            elem = definition.build_elem(dom)
            elems.append(elem)

        return elems
