#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.06 16:21 +0600

Farth - an attempt to implement Forth.
"""

import re

from Farth.funcs import Funcs, FarthError

from Farth.vm import FarthVM

VERSION = "0.7.0"
DEF_WORD = ":"
END_DEF_WORD = ";"
PLUS = "+"
MINUS = "-"
MODULO = "%"
DIV = "/"
MUL = "*"
DUP = "dup"
DO = "do"
LOOP = "loop"
EQUAL = "="
NOT_EQUAL = "!="
LESS_OR_EQUAL = "<="
GREATER_OR_EQUAL = ">="
LESS = "<"
GREATER = ">"
PRINT = "print"
IF = "if"
ELSE = "else"
ENDIF = "endif"
DROP = "drop"
SWAP = "swap"
ROT = "rot"
OVER = "over"
CP_FROM_LOOP_STACK = "i"
ADD_TO_LOOP_STACK = "la"
INCLUDE = "include"
COMMENT = "#"
PRINT_STACK = ".s"
FORGET = "forget"
DDUP = "2" + DUP
DSWAP = "2" + SWAP
DDROP = "2" + DROP
DOVER = "2" + OVER
REVERSE = "rs"
LOWER = "lower"
UPPER = "upper"
TOSTR = "tostr"
STR_INDEX = "stri"
STR_SLICE = "slice"
STR_LEN = "strlen"
SIZEOF = "sizeof"
STR_REVERSE = "strrs"
QUIT = ".quit"
DIS = ".dis"

class Farth(object):
	"""Main Farth class"""
	
	def __init__(self):
		self.vm = FarthVM('', self)
		
		# List of words
		self.words = {DEF_WORD: Funcs.do_def,
			END_DEF_WORD: Funcs.do_enddef,
			PLUS: Funcs.do_plus,
			MINUS: Funcs.do_minus, MUL: Funcs.do_mul,
			DIV: Funcs.do_div,
			MODULO: Funcs.do_modulo, DROP: Funcs.drop,
			PRINT: Funcs.do_print, DO: Funcs.do_do,
			DUP: Funcs.dup, IF: Funcs.do_if, LOOP: Funcs.do_loop,
			EQUAL: Funcs.equal, NOT_EQUAL: Funcs.not_equal,
			LESS_OR_EQUAL: Funcs.less_or_equal,
			GREATER_OR_EQUAL: Funcs.greater_or_equal,
			ENDIF: Funcs.do_endif, INCLUDE: Funcs.do_include,
			ADD_TO_LOOP_STACK: Funcs.do_add_to_loop_stack,
			COMMENT: Funcs.do_pass, ELSE: Funcs.do_else,
			CP_FROM_LOOP_STACK: Funcs.do_cp_from_loop_stack,
			SWAP: Funcs.do_swap, ROT: Funcs.do_rotate,
			OVER: Funcs.do_over, PRINT_STACK: Funcs.print_stack,
			FORGET: Funcs.forget, DDUP: Funcs.do_2dup,
			DSWAP: Funcs.do_2swap, DDROP: Funcs.do_2drop,
			DOVER: Funcs.do_2over, LESS: Funcs.less,
			GREATER: Funcs.greater, REVERSE: Funcs.reverse_stack,
			LOWER: Funcs.lower, UPPER: Funcs.upper, TOSTR: Funcs.to_str,
			STR_INDEX: Funcs.str_index, STR_SLICE: Funcs.str_slice,
			STR_LEN: Funcs.str_len, SIZEOF: Funcs.sizeof,
			STR_REVERSE: Funcs.str_reverse, QUIT: Funcs.do_quit,
			DIS: Funcs.dis}

		# Position in code
		self.pos = (1, 1)
		self.i = 0
		# Code
		self.code = {}
		self.code_str = ""
		# Line number of last commented line
		self.comment = None
		self.def_just_started = False
		
	def find_words(self, s):
		"""Brick string by lines and words"""
		
		found_words = {}
		lines = s.split("\n")
		for i in range(len(lines)):
			words_ = re.findall(r'(".*?"|[^ ]+)', lines[i])
			j = 1
			for word in words_:
				if word:
					found_words[(i+1, j)] = word
				j += len(word) + 1
		
		return found_words
	
	def compile_list(self, words):
		"""Execute Farth code from list like ['1', '2', '3']"""

		if len(words) > 0:
			string = words[0]
			if len(words) > 1:
				for word in words[1:]:
					string += " " + word
			
			self.compile_string(string)
	
	def debug(self):
		"""Prints things like stack length, position and some other things."""
		
		print("================")
		print("stack length: %d" %len(self.vm.stack))
		print("code: %s" %self.code)
		print("def_n: %d" %self.vm.def_n)
		print("def_stack length: %d" %len(self.vm.def_stack))
		print("if_n: %d" %self.vm.if_n)
		print("if_list: %d" %self.vm.if_list)
		print("loop_n: %d" %self.vm.loop_n)
		print("loop_list length: %d" %len(self.vm.loop_list))
		print("pos: %d:%d" %(self.pos[0], self.pos[1]))
		print("i: %d" %self.i)
		print("================")
	
	def compile(self, found_words, isWord=False):
		"""Execute code"""
		
		keys = sorted(list(found_words.keys()))
		
		if isWord:
			pos = (1, 1)
			i = 0
		else:
			pos = self.pos
			i = self.i
		
		while i < len(keys):
			pos = keys[i]
			word = found_words[pos]
			i += 1
			
			if not isWord:
				self.pos = pos
				self.i = i
			
			if self.pos[0] == self.comment or len(word) == 0:
				continue
			elif word[0] in '0123456789"' and word not in self.words:
				if word[0] in '"':
					word = "'%s'" %word
				self.vm.program.append(["PUSH", word])
			elif word == COMMENT:
				self.comment = pos[0]
			else:
				if self.def_just_started:
					self.vm.program.append(["DEFPUSH", '"%s"' %word])
					self.def_just_started = False
				else:
					if word in self.words:
						self.words[word](self.vm)
					else:
						self.vm.program.append(["EWORD", '"%s"' %word])
	
	def compile_string(self, s, add_newline=True, custom_word=False):
		"""Execute code from string"""
		
		if not custom_word:
			self.code_str += s
			if add_newline:
				self.code_str += "\n"
			else:
				self.code_str += " "
			
			found_words = self.find_words(self.code_str)
			self.code.update(found_words)
			self.compile(self.code)
		else:
			found_words = self.find_words(s)
			self.compile(found_words, isWord=True)
	
	def compile_and_execute(self, s):
		try:
			for i in re.findall(r'(".*?"|[^ ]+)', s):
				self.compile_string(i, add_newline=False)
				self.vm.execute()
		finally:
			self.code_str += "\n"
