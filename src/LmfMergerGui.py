#!/usr/bin/env python

# Graphical interface for invoking LmfMerger

TEST_FILE1 = '/data/home/michel/diplomka/lmfmerge/lmf/encoding/iso-8859-2.xml'
TEST_FILE2 = '/data/home/michel/diplomka/lmfmerge/lmf/encoding/iso-8859-2.xml'

import pygtk
pygtk.require('2.0')
import gtk
import threading
import gobject

import LmfMerger

class LmfMergerThread(threading.Thread):
	def __init__(self, gui, filename1, filename2, outfile):
		super(LmfMergerThread, self).__init__()
		self.__gui = gui
		self.__filename1 = filename1
		self.__filename2 = filename2
		self.__outfile = outfile
		self.quit = False

	def __add_message_cb(self, message, wrap):
		self.__gui.add_message(message, wrap)
		return False

	def add_message(self, message, wrap):
		gobject.idle_add(self.__add_message_cb, message, wrap)

	def run(self):
		gui = self.__gui
		merger = LmfMerger.LmfMerger(self.__filename1, self.__filename2, self.__outfile, self)



class LmfMergerGui:
	filebox_list = list() # array of VBoxes
	outfile = "lmf-merger_OUTPUT/_merger_output.xml"

	def delete_event(self, widget, event, data=None):
		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False


	def destroy(self, widget, data=None):
		gtk.main_quit()


	def merge(self, widget, data=None):
		"""Runs merge on selected files"""
		filename1 = self.filebox_list[0].entry.get_text()
		filename2 = self.filebox_list[1].entry.get_text()
		t = LmfMergerThread(self, filename1, filename2, "_merger_output.xml")
		t.start()
		t.quit()


	def browse(self, widget, data=None):
		fb = self.filebox_list[widget.id]
		fb.file_selection.show()

	def file_ok_sel(self, widget, data=None):
		fb = self.filebox_list[data]
		fb.entry.set_text(fb.file_selection.get_filename())
		fb.file_selection.hide()

	def file_cancel_sel(self, widget, data=None):
		fb = self.filebox_list[data]
		fb.file_selection.hide()


	def create_fileboxes(self, count):
		"""Creates 'count' columns for processing/merging a file"""
		for i in range(0, count):
			self.filebox_list.append( gtk.VBox(False, 5) )

			fb = self.filebox_list[i]

			# file selection
			fb.file_selection = gtk.FileSelection('Select LMF file')
			fb.file_selection.cancel_button.connect("clicked", self.file_cancel_sel, i)
			fb.file_selection.ok_button.connect("clicked", self.file_ok_sel, i)

			# file input and browse button
			fb.browse_and_entry_box = gtk.HBox(False, 0)
			fb.pack_start(fb.browse_and_entry_box, False, False, 0)
			fb.browse_and_entry_box.show()

			# file input
			fb.entry = gtk.Entry(max=0)
			fb.browse_and_entry_box.pack_start(fb.entry, True, True, 0)
			fb.entry.show()

			# browse button
			fb.bBrowse = gtk.Button("...")
			fb.bBrowse.id = i
			fb.bBrowse.connect("clicked", self.browse)
			fb.browse_and_entry_box.pack_start(fb.bBrowse, False, False, 0)
			fb.bBrowse.show()

			# file content entry
			fb.content_view = gtk.TextView()
			fb.content_view.id = i
			fb.pack_start(fb.content_view, True, True, 0)
			fb.content_view.show()

			self.filesBox.pack_start(self.filebox_list[i])
			fb.show()


	def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("LMF merging tool")
		# Sets the border width of the window.
		self.window.set_border_width(10)
		self.window.resize(500,600)

		# register delete and destroy events
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		# main VBox
		self.mainVBox = gtk.VBox(False, 10)
		self.window.add(self.mainVBox)
		self.mainVBox.show()

		# tool box
		self.toolBox = gtk.HBox()
		self.mainVBox.pack_start(self.toolBox, False, False, 0)
		self.toolBox.show()

		# Merge button
		self.bMerge = gtk.Button("Merge")
		self.bMerge.connect("clicked", self.merge, None)
		self.toolBox.pack_start(self.bMerge, False, False, 0)
		self.bMerge.show()

		# files box
		self.filesBox = gtk.HBox(False, 10)
		self.mainVBox.pack_start(self.filesBox, True, True, 0)
		self.filesBox.show()

		# create two file boxes
		self.create_fileboxes(2)

		# default files - practical for debugging
		self.filebox_list[0].entry.set_text(TEST_FILE1)
		self.filebox_list[1].entry.set_text(TEST_FILE2)

		# create box with messages
		self.messages_view = gtk.TextView()
		self.mainVBox.pack_start(self.messages_view, False, False, 0)
		self.messages_view.set_editable(False)
		self.messages_view.show()

		# show window
		self.window.show()

	def add_message(self, message, wrap = True):
		self.messages_view.get_buffer().insert_at_cursor(message)

		if wrap == True:
			self.messages_view.get_buffer().insert_at_cursor("\n")

	def main(self):
		# event loop
		gtk.main()

print __name__

gobject.threads_init()

if __name__ == "__main__":
	lmf_merger_gui = LmfMergerGui()
	lmf_merger_gui.main()
