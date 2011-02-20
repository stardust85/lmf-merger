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

class Enumerate(object):
    def __init__(self, names):
        for number, name in enumerate(names.split()):
            setattr(self, name, number)

merge_types = Enumerate('BY_DEFINITION BY_EQUIVALENT BY_BOTH')

import xml.dom.minidom
import language_coding as language_coding_module
import lexical_entry as lexical_entry_module
import synset as synset_module
from lmf_tools import *

class Lexicon:
    """
    Class for storing a LMF lexicon.
    """
    def __init__(self, xmlnode, global_info):
        #
        # parse language
        #
        lang = get_feat(xmlnode, 'lang')
        self.lang = language_coding_module.to_ISO_639_3(lang, global_info.get('language_coding'))

        #
        # load synsets
        #
        ss_elems = xmlnode.getElementsByTagName('Synset')
        self.synsets = dict()
        for ss_elem in ss_elems:
            ss = synset_module.Synset(ss_elem, global_info)
            self.synsets[ss.old_id] = ss

        #
        # parse lexical entries
        #
        lex_entry_nodes = xmlnode.getElementsByTagName('LexicalEntry')
        self.lex_entries = dict()

        for node in lex_entry_nodes:
            lex_entry = lexical_entry_module.LexicalEntry(node, global_info, self)
            if lex_entry.pos not in self.lex_entries:
                self.lex_entries[lex_entry.pos] = dict()

            self.lex_entries[lex_entry.pos][lex_entry.lemma] = lex_entry

        #
        # detect, if it is an explanatory lexicon, or a translation lexicon
        #
        self.has_translations = bool(xmlnode.getElementsByTagName('Equivalent'))
        self.has_definitions =  bool(xmlnode.getElementsByTagName('Definition'))

	
	def get_statistics(self):
		stats = list()
		stats.append('\tLanguage: ' + repr(lexicon.lang)
			for pos in self.lex_entries:
				stats.append('\t\tNumber of lexical entries with partOfSpeech '
				 + pos + ':' str(len(self.lex_entries[pos])))
		stats.append('\t\tNumber of synsets: ' + len(self.synsets)
		return stats

    def update_synset_id(old_id, new_id):
        """updates all references to the synset to its new id"""
        for pos in lex_entries:
            for lex_entry in lex_entries[pos]:
                for sense in lex_entry.sense_list:
                    if sense.synset_id == old_id:
                        sense.synset_id == new_id


    def merge_with_lexicon(self, another):
        """Add content of another lexicon to me"""
        #
        # detection of way how to merge lentries
        #
        if self.has_translations and another.has_definitions:
            # TODO ask user on merging method
            pass
        elif self.has_translations and another.has_translations:
            merge_type = merge_types.BY_EQUIVALENT
        elif self.has_definitions and another.has_definitions:
            merge_type = merge_types.BY_DEFINITION

        #
        # merge synsets
        #

        # merge only (i.e. remove duplicities)
        for another_synset_id in another.synsets:
            we_have_it = False
            # test whether we have it
            for my_synset_id in self.synsets:
                if self.synsets[my_synset_id].equals_to(another.synsets[another_synset_id]):
                    we_have_it = True
                    break

            if we_have_it:
                # change its new id to be compatible
                another.synsets[another_synset_id].new_id = my_synset.old_id
                # update synset references in another
                another.update_synset_id(another_synset_id, my_synset.old_id)
            # we will add it, but with a new id
            else:
                # we have a collision of IDs - add
                if another_synset_id in self.synsets:
                    new_id = get_new_id(self.synsets, another_synset_id)
                    another.synsets[another_synset_id].new_id = new_id
                    ahother.update_synset_id(another_synset_id, new_id)
                    used_id = new_id
                else:
                    used_id = another_synset_id

                self.synsets[used_id] = another.synsets[another_synset_id]


        #
        # merge lexical entries
        #

        # go thru parts of speech in other lexicon
        for pos in another.lex_entries:
            # do I have this part of speech in my lexicon?
            if pos not in self.lex_entries:
                # no, I will add it all from another lexicon
                # (by linking - it is mutable :)
                self.lex_entries[pos] = another.lex_entries
            else:
                # yes, we have to check each lexical entry
                for lemma in another.lex_entries[pos]:
                    if lemma in self.lex_entries[pos]:
                        # we have to merge them
                        self.lex_entries[pos][lemma].merge_with_lex_entry(another.lex_entries[pos][lemma], merge_type)
                    else:
                        # add it
                        self.lex_entries[pos][lemma] = another.lex_entries[pos][lemma]

    def build_elem(self, dom):
        lexicon_elem = dom.createElement('Lexicon')
        add_feat(dom, lexicon_elem, 'lang', self.lang)

        # add lexical entries
        for pos in self.lex_entries:
            for lemma in self.lex_entries[pos]:
                lexicon_elem.appendChild(self.lex_entries[pos][lemma].build_elem(dom))

        # add synsets
        for synset_id in self.synsets:
            print synset_id
            print self.synsets[synset_id]
            lexicon_elem.appendChild(self.synsets[synset_id].build_elem(dom, synset_id))

        return lexicon_elem
