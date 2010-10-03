#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       LmfMerger2.py
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

# system modules
import sys
import xml.dom.minidom
import xml.parsers.expat

# my modules
import LexicalResource

class Enumerate(object):
	def __init__(self, names):
		for number, name in enumerate(names.split()):
			setattr(self, name, number)

msg_types = Enumerate('DEBUG INFO WARNING ERROR')

class LmfMerger:
	def __init__(self, gui = None):
		self.gui = gui

	"""
	Takes two LMF files and merges them into one.
	Just call the constructor and all will be done...
	"""

	def begin(self,whatToPrint):
		"""
		Prints beginning of a message with progress.
		For example 'Sorting numbers...'
		"""
		self.my_print(whatToPrint + ' ...', msg_types.INFO, False)
		sys.stdout.flush()

	def end(self):
		"""
		Prints end of a message with progress. ([DONE])
		"""
		self.my_print("\t[DONE]", msg_types.INFO)

	def my_print(self, message, type, wrap = True):
		"""
		If runs in GUI, prints message to message view.
		If runs in console, displays it to console.
		"""
		if self.gui == None:
			if wrap == True:
				print message
			else:
				print message,
		else:
			self.gui.add_message(message, type, wrap)

	def merge_files(self, file1, file2, outfile):
		"""Runs merging"""

		# build document object models
		try:
			self.begin('building DOM tree from file ' + file1)
			dom1 = xml.dom.minidom.parse(file1)
			self.end()

			self.begin('building DOM tree from file ' + file2)
			dom2 = xml.dom.minidom.parse(file2)
			self.end()
		except xml.parsers.expat.ExpatError as e:
			self.my_print("XML parsing error: " + str(e))
			return

		# create lexical resources
		lr1 = LexicalResource.LexicalResource(dom1.getElementsByTagName('LexicalResource')[0])
		lr2 = LexicalResource.LexicalResource(dom2.getElementsByTagName('LexicalResource')[0])

		# merge lexical resources
		try:
			print 'before merge lr'
			lr2.merge_with_LR(lr1)
			print 'after'
		except LexicalResource.IncompatibleDTDError as e:
			self.my_print("Incompatible DTD versions: File %s has version %s, file %s has version %s"
			% ( file2, e.my_version, file1, e.other_version), msg_types.ERROR);
			return

		# update dom tree of a result
		lr2.update_DOM()

		# write output
		resultxml = lr2.dom.toprettyxml()
		outfiledsc = open(outfile, 'w')
		outfiledsc.write(resultxml.encode("utf-8"))
		outfiledsc.close

		self.my_print("merged file written to " + outfile, msg_types.INFO)

def usage():
	"""Prints how to run this program"""
	print """
Usage:
	./lmf-merger.py file1 file2 outfile
	example: ./lmf-merger.py data/lmf/ac_eko_dlouhe_50_xxx_lmf.xml \
	data/lmf/ac_frs_dlouhe_50_xxx_lmf.xml ac_eko-frs_dlouhe_50_xxx_lmf.xml
	"""

################################################################################
# main
################################################################################

def main():
	# we need two args
	if sys.argv.__len__() != 4:
		usage()
		sys.exit(1)

	# input and output files
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	outfile = 'lmf-merger_OUTPUT/' + sys.argv[3]

	merger = LmfMerger()
	merger.merge_files(file1, file2, outfile)
	return 0

if __name__ == '__main__':
	main()
