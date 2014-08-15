#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Farth import farth
try:
	import readline
except ImportError:
	import pyreadline as readline
import os
import atexit
import sys
import shlex
import struct
import subprocess
import platform
import argparse

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

def colorize(text, color):
	return "\033[%s%s\033[0m" %(color, text)

def prompt():
	if platform.system() == "Windows":
		return input_("Farth %s> " %farth.VERSION)
	else:
		msg = colorize("Farth ", "94m") + colorize(farth.VERSION, "92m") + \
			colorize("> ", "94m")
		return input_(msg)

def dump_vmcode(farth_obj, filename):
	s = farth_obj.vm.gen_string()
	f = open(filename, "w")
	f.write(s)
	f.close()

def invert_dict(d):
	newd = {}
	for i in d:
		newd[d[i]] = i
	
	return newd

import re

def encode(code, bytes_):
	newcode = ''
	
	for i in code.split("\n"):
		j = re.findall(r'(\'".*?"\'|[^ ]+)', i)
		args = "\x98" + "\x98".join(map(str, j[1:])) if len(j) > 1 else ''
		newcode += bytes_[j[0].lower()] + args
		newcode += "\x99"
	
	return newcode[0:-1]

def decode(code, bytes_):
	newcode = ''
	
	for i in code.split("\x99"):
		j = re.findall(r'(\'".*?"\'|[^\x98]+)', i)
		args = " " + " ".join(map(str, j[1:])) if len(j) > 1 else ''
		newcode += bytes_[j[0]] + args
		newcode += "\n"
	
	return newcode[0:-1]

def compile_to_bytecode(code, bytes_, filename):
	bytecode = encode(code, bytes_)
	f = open(filename, "wb")
	f.write(b'FARTHBIN\n')
	f.write(bytes(bytecode, "utf8"))
	f.close()

if __name__ == "__main__":
	f = farth.Farth()
	arg_parser = argparse.ArgumentParser(
		description="Some sort of Forth implementation")
	arg_parser.add_argument("filename", nargs="*", help="File to be executed")
	arg_parser.add_argument("-d", "--dump", action="store_true",
		help="Dump VM code into file")
	arg_parser.add_argument("-b", "--bytecode", action="store_true",
		help="Translate code to VM bytecode")
	arg_parser.add_argument("-o", "--output", nargs=1, help="Output file")
	args = arg_parser.parse_args()
	
	if args.filename:
		try:
			f_ = open(args.filename[0], "r")
			code = f_.read()
			f_.close()
		except IOError:
			print("File '%s' doesn't exist" %args.filename[0])
			sys.exit(1)
		
		if args.dump and args.output:
			f.compile_string(code)
			dump_vmcode(f, args.output[0])
		elif args.bytecode and args.output:
			f.compile_string(code)
			compile_to_bytecode(f.vm.gen_string(), invert_dict(f.vm.bytes),
				args.output[0])
		else:
			if code.startswith("FARTHBIN\n"):
				code = decode(code[9:], f.vm.bytes)
				f.vm = farth.FarthVM(code, f)
				f.vm.execute()
			else:
				f.compile_and_execute(code)
		sys.exit(0)
	
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
		if platform.system() != "Windows":
			print(colorize(msg, "94m"))
		else:
			print(msg)
	
	while True:
		try:
			readline.set_completer(Completer(f.words).complete)
			s = prompt()
			if s:
				f.compile_and_execute(s)
			if f.vm.pc is None:
				raise EOFError
		except EOFError:
			a = input_("\nAre You sure You want to exit? [Y/n]").lower()
			if len(a) == 0 or a == "y":
				sys.exit(0)
		except farth.FarthError as error:
			print(error)
		except KeyboardInterrupt:
			print('')
