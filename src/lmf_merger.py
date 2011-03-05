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

# system modules
import sys
import xml.dom.minidom
import optparse

# my modules
import lexical_resource

class FatalError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return 'FATAL ERROR: ' + self.message

class Enumerate(object):
    def __init__(self, names):
        for number, name in enumerate(names.split()):
            setattr(self, name, number)

msg_types = Enumerate('DEBUG INFO WARNING ERROR')

class LmfMerger:
    """
    Lmf Manager class.
    """
    def __init__(self, gui = None):
        self.gui = gui
        self.in_progress = False

    def begin(self,whatToPrint):
        """
        Prints beginning of a message with progress.
        For example 'Sorting numbers...'
        """
        self.my_print(whatToPrint + ' ...', msg_types.INFO, False)
        self.in_progress = True
        sys.stdout.flush()

    def end(self):
        """
        Prints end of a message with progress. ([DONE])
        """
        self.my_print("\t[DONE]", msg_types.INFO)
        self.in_progress = False

    def my_print(self, message, type, wrap = True):
        """
        If runs in GUI, prints message to message view.
        If runs in console, displays it to console.
        """
        # create newline if was in progress but failed
        if self.in_progress and type == msg_types.ERROR:
            message = '\n' + message
        if wrap == True:
            message = message + '\n'
        if self.gui is None:
            sys.stdout.write(message)
        else:
            self.gui.add_message(message, type)
            
    def print_statistics(filename):
        lr = merger.parse_file(filename)
        stats = lr.get_statistics()
        for line in stat:
            my_print(line, msg_types.INFO)

    def parse_file(filename):
        """Creates LexicalResource object from given file"""
        
        # create DOM tree
        try:
            self.begin('building DOM tree from file ' + filename)
            dom = xml.dom.minidom.parse(filename)
            self.end()

        except xml.parsers.expat.ExpatError as e:
            self.my_print("XML parsing error: " + str(e), msg_types.ERROR)
            raise
        
        # create lexical resource
        try:
            self.begin('Extracting data from DOM of file ' + filename)
            lr = lexical_resource.LexicalResource(dom.getElementsByTagName('LexicalResource')[0])
            self.end()
            return lr
        except FatalError as e:
            self.my_print(str(e), msg_types.ERROR)
            self.my_print('Processing stopped. Please fix the previous error(s) and try it again', msg_types.ERROR)
            raise
       

    def merge_files(self, file1, file2, outfile):
        """Runs merging"""

        try:
            lr1 = parse_file(file1)
            lr2 = parse_file(file2)

            # merge lexical resources
            lr2.merge_with_LR(lr1)

        except Exception as e:
            self.my_print(str(e), msg_types.ERROR)
            self.my_print('Processing stopped. Please fix the previous error(s) and try it again', msg_types.ERROR)
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
Usages:
    ./lmf-merger.py -m file1 file2 outfile
    ./lmf-merger.py -s file1 ...
    example: ./lmf-merger.py data/lmf/ac_eko_dlouhe_50_xxx_lmf.xml \
    data/lmf/ac_frs_dlouhe_50_xxx_lmf.xml ac_eko-frs_dlouhe_50_xxx_lmf.xml
    """

################################################################################
# main
################################################################################

def main():
    parser = optparse.OptionParser()
    parser.add_option("--statistics")
    options, args = parser.parse_args()

    merger = LmfMerger()

    if not options.statistics is None:
        merger.print_statistics(args[1])
        return 0
        
    
    # we need two args
    if sys.argv.__len__() != 4:
        usage()
        sys.exit(1)

    # input and output files
    file1 = args[1]
    file2 = args[2]
    outfile = args[3]

    merger.merge_files(file1, file2, outfile)
    return 0

if __name__ == '__main__':
    main()
