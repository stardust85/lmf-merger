#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       LmfTools.py
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

import xml.dom

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
	matching_subnodes = list()

	for child in node.childNodes:
		if child.nodeType == xml.dom.Node.ELEMENT_NODE and child.nodeName == tagname:
			matching_subnodes.append(child)

	return matching_subnodes

def get_feat(node, name):
	"""
	Returns value of given attribute name name in any feature of the node
	"""

	value = None
	feats = node.getElementsByTagName('feat')
	for feat in feats:
		if feat.attributes['att'].value == name:
			value = feat.attributes['val'].value
			break
	return value

def get_feats(node):
	"""
	Returns dictionary of features and its values.
	"""
	feats = node.getElementsByTagName('feat')
	result = dict()
	for feat in feats:
		result[feat.attributes['att'].value] = feat.attributes['val'].value
	return result

#def merge_feats(feats1, feats2):
##	Merges feats1 to feats2. Returns merged feats2.
#	"""
#	for feat in feats1:
#		if feat in feats2:
