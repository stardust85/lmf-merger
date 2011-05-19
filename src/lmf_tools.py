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

import re

def get_new_id(existing_ids, colliding_id):
    new_id_found = False
    i = 1
    while not new_id_found:
        another_synset_id_new = another_synset_id + '_coll' + str(i)
        if another_synset_id_new not in self.synsets:
            return another_synset_id_new
        i += 1

def get_words(text):
    """
    Splits a sentence to words.
    """
    text = re.sub('[^\w&^\d]', ' ', text) # convert special symbols to spaces
    text = text.lower()
    return text.split()

def get_child_elements(node, tagname):
    """
    Returns list of direct subnodes of type ELEMENT (=sub-elements)co
    of given tag name.
    """
    return node.findall(tagname)

def get_feat(node, name):
    """
    Returns value of given attribute name name in any feature of the node
    """

    value = None
    feats = node.findall('feat')
    for feat in feats:
        if feat.get('att') == name:
            value = feat.get('val')
            break
    return value


def get_part_of_speech(node):
    """ returns part-of-speech of given node, or 'missing' if not found"""
    value = get_feat(node, 'partOfSpeech')

    if value == None:
        value = get_feat(node, 'pos')

    return value


def get_feats(node):
    """
    Returns dictionary of features and its values.
    """
    feats = node.findall('feat')
    result = dict()
    for feat in feats:
        result[feat.get('att')] = feat.get('val')
    return result


def add_feat(dom, elem, name, value):
    if value != None:
        feat = dom.createElement('feat')
        feat.setAttribute('att', name)
        feat.setAttribute('val', value)
        elem.appendChild(feat)



#def merge_feats(feats1, feats2):
##  Merges feats1 to feats2. Returns merged feats2.
#   """
#   for feat in feats1:
#       if feat in feats2:
