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
import lmf_merger
import lexicon as lexicon_module


DEFAULT_DTD_VERSION = "16"
DEFAULT_LANGUAGE_CODING = "ISO 639-3"


class LexicalResource:
    """
    Class for manipulation with LMF lexical resources.
    """

    def __init__(self, xmlnode):
        """
        Reads information from LMF root node into python data structures.
        """
        # read DTD version
        self.dtdVersion = xmlnode.attrib.get('dtdVersion')

        # only version 16 supported for now
        if self.dtdVersion != '16':
            raise lmf_merger.FatalMergeError('DTD version %d not supported. Please upgrade to version 16')

        #
        # read global information
        #
        gi_node = get_child_elements(xmlnode, 'GlobalInformation')[0]
        self.global_info = get_feats(gi_node)

        # language coding
        language_coding = self.global_info.get('languageCoding')

        # read lexicons
        self.lexicons = dict()
        lexicon_nodes = get_child_elements(xmlnode, 'Lexicon')
        for node in lexicon_nodes:
            my_lexicon = lexicon_module.Lexicon(node, self.global_info)

            # is there already a lexicon with same lang?
            if(my_lexicon.lang in self.lexicons):
                self.lexicons[my_lexicon.lang].merge_with_lexicon(my_lexicon)
            else:
                self.lexicons[my_lexicon.lang] = my_lexicon

    def get_statistics(self):
        stats = list() # of lines
        stats.append( 'Number of lexicons: ' + str(len(self.lexicons)))
        for nr, lexicon in enumerate(self.lexicons):
            stats.append('\tLexicon nr.' + str(nr + 1) + ':')
            stats += self.lexicons[lexicon].get_statistics()
            stats += '' # separator
        return stats

    def merge_with_LR(self, anotherLR):
        """
        Adds to myself data from another lexical resource.
        """

        #
        # merge lexicons
        #
        for lang in anotherLR.lexicons:
            # do I have this language?
            if lang in self.lexicons:
                self.lexicons[lang].merge_with_lexicon(anotherLR.lexicons[lang])
            else:
                self.lexicons[lang] = anotherLR.lexicons[lang]


    def update_DOM(self):
        domImplementation = xml.dom.minidom.getDOMImplementation()
        dtd = domImplementation.createDocumentType('LexicalResource', None, "DTD_LMF_REV_16.dtd")
        self.dom = domImplementation.createDocument(None, 'LexicalResource', dtd)

        # add dtd version
        self.dom.documentElement.setAttribute('dtdVersion', DEFAULT_DTD_VERSION)

        # add global information
        gi_elem = self.dom.createElement('GlobalInformation')
        add_feat(self.dom, gi_elem, 'languageCoding', 'ISO 639-3')
        self.dom.documentElement.appendChild(gi_elem)

        # add lexicons
        for lexicon in self.lexicons:
            self.dom.documentElement.appendChild(self.lexicons[lexicon].build_elem(self.dom))
