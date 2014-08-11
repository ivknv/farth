#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.06 16:21 +0600

Farth - an attempt to implement Forth
"""

import re

try:
	from funcs import Funcs, FarthError, StackUnderflow
except ImportError:
	from Farth.funcs import Funcs, FarthError, StackUnderflow

VERSION = "0.3.6"

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

class Farth(object):
	"""Main Farth class"""
	
	def __init__(self):
		# List of default available words
		# Every function must take Farth object as only argument
		self.words = {DEF_WORD: Funcs.do_pass,
			END_DEF_WORD: Funcs.do_pass,
			PLUS: Funcs.do_plus,
			MINUS: Funcs.do_minus, MUL: Funcs.do_mul,
			DIV: Funcs.do_div,
			MODULO: Funcs.do_modulo, DROP: Funcs.drop,
			PRINT: Funcs.do_print, DO: Funcs.do_pass,
			DUP: Funcs.dup, IF: Funcs.do_pass, LOOP: Funcs.do_pass,
			EQUAL: Funcs.equal, NOT_EQUAL: Funcs.not_equal,
			LESS_OR_EQUAL: Funcs.less_or_equal,
			GREATER_OR_EQUAL: Funcs.greater_or_equal,
			ENDIF: Funcs.do_pass, INCLUDE: Funcs.do_include,
			ADD_TO_LOOP_STACK: Funcs.do_add_to_loop_stack,
			COMMENT: Funcs.do_pass, ELSE: Funcs.do_pass,
			CP_FROM_LOOP_STACK: Funcs.do_cp_from_loop_stack,
			SWAP: Funcs.do_swap, ROT: Funcs.do_rotate,
			OVER: Funcs.do_over, PRINT_STACK: Funcs.print_stack,
			FORGET: Funcs.forget, DDUP: Funcs.do_2dup,
			DSWAP: Funcs.do_2swap, DDROP: Funcs.do_2drop,
			DOVER: Funcs.do_2over, LESS: Funcs.less,
			GREATER: Funcs.greater}
		
		# Data stack
		self.stack = []
		# Stack for defining words
		self.def_stack = []
		self.def_n = 0
		# Stack for if-else statements
		self.if_list = []
		self.if_n = 0
		self.else_n = 0
		# Loop stack
		self.loop_list = []
		self.loop_n = 0
		# Position in code
		self.pos = (1, 1)
		self.i = 0
		# Code
		self.code = {}
		self.code_str = ""
		# Number of last commented line
		self.comment = None
		
	def find_words(self, s):
		"""Brick string by lines and words"""
		
		found_words = {}
		lines = s.split("\n")
		for i in range(len(lines)):
			words_ = re.findall(r'(".*?"|[^ ]+)', lines[i])
			j = 1
			for word in words_:
				found_words[(i+1, j)] = word
				j += len(word) + 1
		
		return found_words

	def def_word(self, def_stack):
		"""Define new word"""
		
		try:
			word = def_stack[0]
		except IndexError:
			raise FarthError(self, "Word definition is empty")
		word_body = def_stack[1:]
		new_word = word_body[0]
		if len(word_body) > 1:
			for w in word_body[1:]:
				new_word += " "+w
		
		self.words[word] = lambda obj: obj.execute_string(new_word, custom_word=True)
	
	def execute_list(self, words):
		"""Execute Farth code from list like ['1', '2', '3']"""

		if len(words) > 0:
			string = words[0]
			if len(words) > 1:
				for word in words[1:]:
					string += " " + word
			
			self.execute_string(string)
	
	def debug(self):
		"""Prints things like stack length, position and some other things."""
		
		print("================")
		print("stack length: %d" %len(self.stack))
		print("code: %s" %self.code)
		print("def_n: %d" %self.def_n)
		print("def_stack length: %d" %len(self.def_stack))
		print("if_n: %d" %self.if_n)
		print("if_list length: %d" %len(self.if_list))
		print("loop_n: %d" %self.loop_n)
		print("loop_list length: %d" %len(self.loop_list))
		print("pos: %d:%d" %(self.pos[0], self.pos[1]))
		print("i: %d" %self.i)
		print("================")
	
	def execute(self, found_words, isWord=False):
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
			elif self.def_n > 0:
				if word != END_DEF_WORD or self.def_n > 1:
					if word == DEF_WORD:
						self.def_n += 1
					elif word == END_DEF_WORD:
						self.def_n -= 1
					self.def_stack.append(word)
				else:
					self.def_n -= 1
					if self.def_n < 1:
						self.def_word(self.def_stack)
						self.def_stack = []
			elif self.if_n > 0:
				if word == ELSE and self.if_n == 1:
					self.else_n = 1
				elif self.else_n == 1 and (word != ENDIF or self.if_n > 1):
					if word == ENDIF:
						self.if_n -= 1
					elif word == IF:
						self.if_n += 1
					self.if_list[1].append(word)
				elif word != ENDIF or self.if_n > 1:
					if word == IF:
						self.if_n += 1
					elif word == ENDIF:
						self.if_n -= 1
					self.if_list[0].append(word)
				else:
					body = self.if_list[0]
					else_body = self.if_list[1]
					self.if_list[0], self.if_list[1] = [], []
					self.if_n -= 1
					self.else_n -= 1
					
					try:
						if self.stack.pop() == 1:
							self.execute_list(body)
						else:
							if len(else_body) > 0:
								self.execute_list(else_body)
					except IndexError:
						raise StackUnderflow(self)
			elif self.loop_n > 0 and self.loop_list and word == LOOP:
				if self.loop_list[self.loop_n-1][0] > 1:
					self.loop_list[self.loop_n-1][0] -= 1
					pos = self.loop_list[self.loop_n-1][1]
					i = keys.index(pos)
					if not isWord:
						self.pos = pos
						self.i = i
				else:
					del self.loop_list[self.loop_n-1]
					self.loop_n -= 1
			elif word[0] in '0123456789"' and word not in self.words:
				self.stack.append(eval(word))
			elif word == IF:
				self.if_n += 1
				self.if_list.append([])
				self.if_list.append([])
			elif word == DEF_WORD:
				self.def_n += 1
			elif word == DO:
				try:
					self.loop_list.append([self.stack.pop()])
				except IndexError:
					raise StackUnderflow(self)
				self.loop_list[self.loop_n].append(keys[keys.index(pos)+1])
				self.loop_n += 1
			elif word == COMMENT:
				self.comment = pos[0]
			else:
				try:
					func = self.words[word]
				except KeyError:
					raise FarthError(self, "Unknown word")
				
				res = func(self)
				if res is not None:
					self.stack.append(res)
	
	def execute_string(self, s, add_newline=True, custom_word=False):
		"""Execute code from string"""
		
		if not custom_word:
			self.code_str += s
			if add_newline:
				self.code_str += "\n"
			else:
				self.code_str += " "
			found_words = self.find_words(self.code_str)
			self.code.update(found_words)
			self.execute(self.code)
		else:
			found_words = self.find_words(s)
			self.execute(found_words, isWord=True)
