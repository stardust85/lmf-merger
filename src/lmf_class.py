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
import lxml.etree as ET

class LmfClass:
    allowed_feats = set(['writtenForm', 'phoneticForm'])
    def __init__(self, xmlnode):
        self.feats = get_feats(xmlnode)
        
    def build_elem(self, parent):
        elem = ET.SubElement(parent, self.__class__.__name__)
        for feat in self.feats:
            if feat in LmfClass.allowed_feats:
                add_feat(elem, feat, self.feats[feat])
        return elem
