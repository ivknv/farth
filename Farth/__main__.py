#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Farth import farth
import readline
import os
import atexit
import sys

try:
	input_ = raw_input
except NameError:
	input_ = input

histpath = os.path.expanduser("~/.farth_history")
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set editing-mode vi")

def on_exit():
	readline.write_history_file(histpath)

class Completer(object):
	def __init__(self, options):
		self.options = sorted(options)
	
	def complete(self, text, state):
		if state == 0:
			if text:
				self.matches = [s for s in self.options
					if s and s.startswith(text)]
			else:
				self.matches = self.options
		
		try:
			response = self.matches[state]
		except IndexError:
			response = None
		
		return response

if __name__ == "__main__":
	f = farth.Farth()
	
	readline.set_completer(Completer(f.words).complete)
	
	if os.path.exists(histpath):
		readline.read_history_file(histpath)
	
	atexit.register(on_exit)
	
	msg = r"""
    ///////  ///\\\         /////////  ///////////  ///
   ///      ///  \\\       ///   ///      ///      ///
  //////// /////\\\\\     /////////      ///      /////////
 ///      //////\\\\\\   ///\\\         ///      ///   ///
///      ///        \\\ ///  \\\       ///      ///   ///

Some sort of Forth implementation"""[1:]
	
	print("\033[94m%s\033[0m" %msg)
	
	s = ''
	while s != ".quit":
		try:
			readline.set_completer(Completer(f.words).complete)
			if s:
				f.execute_string(s)
			s = input_("\033[94mFarth \033[92m%s\033[94m>\033[0m " %farth.VERSION)
		except EOFError:
			a = input_("\nAre You sure You want to exit? [Y/n]").lower()
			if len(a) == 0 or a == "y":
				sys.exit(0)
		except KeyboardInterrupt:
			print('')
