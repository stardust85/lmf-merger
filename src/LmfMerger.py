#!/usr/local/bin/python

import sys
import xml.dom
import xml.dom.minidom
import xml.parsers.expat

import LmfMergerGui



class LmfNormalizer:
	def __filter_node(self, node):
		"""Removes all duplicate sub-nodes. Works recursively."""
		node.childNodes = list(set(node.childNodes))

		for subnode in node.childNodes:
			self.__filter_node(subnode)

	def filter_senses(self):
		"""Removes exactly same senses"""
		lex_entries = self.dom.getElementsByTagName('LexicalEntry')
		for lex_entry in lex_entries:
			self.__filter_node(lex_entry)

	def remove_whitespace_nodes(self, node, unlink=False):
		"""
		Removes all of the whitespace-only text descendants of a DOM node.

		When creating a DOM from an XML source, XML parsers are required to
		consider several conditions when deciding whether to include
		whitespace-only text nodes. This function ignores all of those
		conditions and removes all whitespace-only text descendants of the
		specified node. If the unlink flag is specified, the removed text
		nodes are unlinked so that their storage can be reclaimed. If the
		specified node is a whitespace-only text node then it is left
		unmodified.

		http://code.activestate.com/recipes/303061/ (r2)
		"""
		remove_list = []
		for child in node.childNodes:
			if child.nodeType == xml.dom.Node.TEXT_NODE and \
		   		not child.data.strip():
				remove_list.append(child)
			elif child.hasChildNodes():
				self.remove_whitespace_nodes(child, unlink)
		for node in remove_list:
			node.parentNode.removeChild(node)
		if unlink:
			node.unlink()

	def __init__(self, dom):
		self.dom = dom


	def normalize_all(self):
		self.remove_whitespace_nodes(self.dom)
		self.filter_senses()
		return self.dom

class LmfMerger:
	"""
	Takes two LMF files and merges them into one.
	Just call the constructor and all will be done...
	"""

	def begin(self,whatToPrint):
		"""
		Prints beginning of a message with progress.
		For example 'Sorting numbers...'
		"""
		self.my_print(whatToPrint + ' ...', False)
		sys.stdout.flush()

	def end(self):
		"""
		Prints end of a message with progress. ([DONE])
		"""
		self.my_print("\t[DONE]")

	def get_feat(self, node, name):
		"""Returns value of given attribute name name in any feature of the node"""

		value = None
		feats = node.getElementsByTagName('feat')
		for feat in feats:
			if feat.attributes['att'].value == name:
				value = feat.attributes['val'].value
				break
		return value

	def get_part_of_speech(self, node):
		""" returns part-of-speech of given node, or 'missing' if not found"""
		value = self.get_feat(node, 'partOfSpeech')

		if value == None:
			value = self.get_feat(node, 'pos')

		if value == None:
			partOfSpeech = 'missing'

		return value

	def compare_senses(sense1, sense2):
		"""
		Returns similarity ranks of two leaf-node senses.

		1. removes too frequent words (they don't contain the important things)
		2. counts how many words from first set is in the second and vice-versa

		"""
		pass

	def merge_senses(self, sense1, sense2):
		"""
		Takes two nodes with <Sense> (they must be on the same level)
		and looks to their contents. If it is too similar, asks user
		which sense (definition) he prefers and adds the selected one.
		If the senses are too different, adds both.
		"""
		pass

	def merge_lexical_entries(self, lex_entry1, lex_entry2):
		"""Adds contents of xml node lex_entry1 to xml node lex_entry2"""
		pass


	def parse_lmf_data(self, dom):
		"""
		Adds new properties to lexical entries (for easier access).

		Future plan (for its own project):
		  Create (or find if someone did it already) a python module,
		  that will recieve XML Schema (or DTD) and xml file and will
		  produce a python structure from it.
		"""

		dom.lexicon = dom.getElementsByTagName('Lexicon')[0]

		dom.lex_entries = dom.getElementsByTagName('LexicalEntry')
		dom.lemma_written_forms = dict()
		dom.lex_entry_dict = dict() # maps lemma written froms to DOM nodes

		for lex_entry in dom.lex_entries:
			lex_entry.lemma = lex_entry.getElementsByTagName('Lemma')[0]
			lex_entry.lemma.written_form = self.get_feat(lex_entry.lemma, 'writtenForm')
			lex_entry.part_of_speech = self.get_part_of_speech(lex_entry.lemma)
			if not (lex_entry.part_of_speech in dom.lemma_written_forms):
				# new part of speech
				dom.lemma_written_forms[lex_entry.part_of_speech] = set()
			dom.lemma_written_forms[lex_entry.part_of_speech].add(lex_entry.lemma.written_form)
			dom.lex_entry_dict[lex_entry.lemma.written_form] = lex_entry

	def merge_doms(self, dom1, dom2):
		"""Adds lexical entries from dom1 to dom2. Returns merged dom2"""

		# extract useful data
		self.parse_lmf_dom(dom1)
		self.parse_lmf_dom(dom2)

		self.my_print("dom2 no pos forms" + str(dom2.lemma_written_forms))

		# zjistit jestli je v druhym dany lexical entry. Kdyz ne, pridat. Kdyz jo, provest merge
		for lex_entry1 in dom1.lex_entries:
			self.my_print("wf " + lex_entry1.lemma.written_form)
			# kouknem jestli je nas writtenform z file1 v odpovidajicim writtenforms2 z Lemmas2
			if lex_entry1.lemma.written_form in dom2.lemma_written_forms[lex_entry1.part_of_speech]:
				# there is already a lexical entry in dom2 with same lemma
				self.merge_lexical_entries(lex_entry1, dom2.lex_entry_dict[lex_entry1.lemma.written_form])
				self.my_print("lentry1 " + lex_entry1.toxml() + "merged")
			else:
				# no lexical entry with same lemma in dom2, we can add the whole lex_entry1
				dom2.lexicon.appendChild(lex_entry1)
				self.my_print("lentry1 " + lex_entry1.toxml() + "appended")

		return dom2

	def my_print(self, message, wrap = True):
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
			self.gui.add_message(message, wrap)

	def try_parse_dom(self, file):
		try:
			return xml.dom.minidom.parse(file)
		except xml.parsers.expat.ExpatError as e:
			self.my_print("XML parsing error: " + str(e))
			return None

	def __init__(self, file1, file2, outfile, gui = None):
		"""Runs merging"""

		self.gui = gui

		# build document object models
		# TODO replace parse with parsestring and recode the string first
		self.begin('building DOM tree from file ' + file1)
		dom1 = self.try_parse_dom(file1)
		self.end()

		self.begin('building DOM tree from file ' + file2)
		dom2 = self.try_parse_dom(file2)
		self.end()

		# something went wrong while parsing files
		if (dom1 == None) or (dom2 == None):
			return

		# normalize DOMs
		dom1 = LmfNormalizer(dom1).normalize_all()
		dom2 = LmfNormalizer(dom2).normalize_all()

		# merge doms
		result = self.merge_doms(dom1, dom2)

		# write output
		resultxml = result.toprettyxml()
		outfiledsc = open(outfile, 'w')
		outfiledsc.write(resultxml.encode("utf-8"))
		outfiledsc.close

		self.my_print("merged file written to " + outfile)


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

if __name__ == "__main__":
	# we need two args
	if sys.argv.__len__() != 4:
		usage()
		sys.exit(1)

	# input and output files
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	outfile = 'lmf-merger_OUTPUT/' + sys.argv[3]

	LmfMerger(file1, file2, outfile)
