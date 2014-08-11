#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Farth import farth
import readline
import os
import atexit
import sys
import shlex
import struct
import subprocess
import platform

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

def get_terminal_size():
	""" getTerminalSize()
	 - get width and height of console
	 - works on linux,os x,windows,cygwin(windows)
	 originally retrieved from:
	 http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
	"""
	current_os = platform.system()
	tuple_xy = None
	if current_os == 'Windows':
		tuple_xy = _get_terminal_size_windows()
		if tuple_xy is None:
			tuple_xy = _get_terminal_size_tput()
			# needed for window's python in cygwin's xterm!
	if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
		tuple_xy = _get_terminal_size_linux()
	if tuple_xy is None:
		tuple_xy = (80, 25)	  # default value
	return tuple_xy 
 
def _get_terminal_size_windows():
	try:
		from ctypes import windll, create_string_buffer
		# stdin handle is -10
		# stdout handle is -11
		# stderr handle is -12
		h = windll.kernel32.GetStdHandle(-12)
		csbi = create_string_buffer(22)
		res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
		if res:
			(bufx, bufy, curx, cury, wattr,
			 left, top, right, bottom,
			 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
			sizex = right - left + 1
			sizey = bottom - top + 1
			return sizex, sizey
	except:
		pass
 

def _get_terminal_size_tput():
	try:
		cols = int(subprocess.check_call(shlex.split('tput cols')))
		rows = int(subprocess.check_call(shlex.split('tput lines')))
		return (cols, rows)
	except:
		pass
 
 
def _get_terminal_size_linux():
	def ioctl_GWINSZ(fd):
		try:
			import fcntl
			import termios
			cr = struct.unpack('hh',
			   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
			return cr
		except:
			pass
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except:
			pass
	if not cr:
		try:
			cr = (os.environ['LINES'], os.environ['COLUMNS'])
		except:
			return None
	return int(cr[1]), int(cr[0])

if __name__ == "__main__":
	f = farth.Farth()
	
	if os.path.exists(histpath):
		readline.read_history_file(histpath)
	
	atexit.register(on_exit)
	
	msg = r"""
    ///////  ///\\\         ////////  ///////////  ///   ///
   ///      ///  \\\       ///  ///      ///      ///   ///
  //////// ///____\\\     ////////      ///      /////////
 ///      ///______\\\   ///\\\        ///      ///   ///
///      ///        \\\ ///  \\\      ///      ///   ///

Some sort of Forth implementation"""[1:]
	
	w = get_terminal_size()[0]
	
	if w >= 60:
		print("\033[94m%s\033[0m" %msg)
	
	i_before = f.i
	
	while True:
		try:
			readline.set_completer(Completer(f.words).complete)
			s = input_("\033[94mFarth \033[92m%s\033[94m>\033[0m " %farth.VERSION)
			if s:
				f.execute_string(s)
			elif s == ".quit":
				sys.exit(0)
		except EOFError:
			a = input_("\nAre You sure You want to exit? [Y/n]").lower()
			if len(a) == 0 or a == "y":
				sys.exit(0)
		except farth.FarthError as error:
			print(error)
			f.i += f.i - i_before - 1
		except KeyboardInterrupt:
			print('')
		else:
			i_before = f.i
