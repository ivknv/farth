#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.06 16:21 +0600

Farth - an attempt to implement Forth
"""

import re
from inspect import ismethod

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
PRINT = "print"
IF = "if"
ELSE = "else"
ENDIF = "endif"
RM = "."
CP_FROM_LOOP_STACK = "i"
RM_FROM_LOOP_STACK = ".l"
INCLUDE = "include"

class Farth(object):
	"""Main Farth class"""
	
	def __init__(self):
		# List of default available words
		self.words = {DEF_WORD: self.do_pass,
			END_DEF_WORD: self.do_pass,
			PLUS: lambda x, y: x+y,
			MINUS: lambda x, y: x-y, MUL: lambda x, y: x*y,
			DIV: lambda x, y: float(x)/float(y),
			MODULO: lambda x, y: x%y, RM: self.remove_from_stack,
			PRINT: self.do_print, DO: self.do_pass,
			DUP: self.dup, IF: self.do_pass, LOOP: self.do_pass,
			EQUAL: self.equal, NOT_EQUAL: self.not_equal,
			LESS_OR_EQUAL: self.less_or_equal,
			GREATER_OR_EQUAL: self.greater_or_equal,
			ENDIF: self.do_pass, INCLUDE: self.do_include,
			RM_FROM_LOOP_STACK: self.do_rm_from_loop_stack,
			CP_FROM_LOOP_STACK: self.do_cp_from_loop_stack, ELSE: self.do_pass}
		
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
	
	def do_pass(self):
		"""Do nothing. This function mostly used as a stub."""
		
		pass
	
	def do_print(self, s):
		"""Print last value in stack"""
		
		print(s)
	
	def dup(self):
		"""Duplicate last value in stack"""
		
		self.stack.append(self.stack[-1])
	
	def do_cp_from_loop_stack(self):
		"""Copy value from loop stack"""
		
		self.stack.append(self.loop_list[-1][0])
	
	def equal(self):
		"""=="""
		
		left = self.stack.pop()
		right = self.stack.pop()
		self.stack.append(1 if left == right else 0)
	
	def not_equal(self):
		"""!="""
		
		left = self.stack.pop()
		right = self.stack.pop()
		self.stack.append(1 if left != right else 0)
	
	def less_or_equal(self):
		"""<="""
		
		left = self.stack.pop()
		right = self.stack.pop()
		self.stack.append(1 if left <= right else 0)
	
	def greater_or_equal(self):
		""">="""
		
		left = self.stack.pop()
		right = self.stack.pop()
		self.stack.append(1 if left >= right else 0)
	
	def do_include(self, filename):
		"""Include code from file"""
		
		f = open(filename)
		code = f.read()
		f.close()
		self.execute_string(code)
	
	def remove_from_stack(self):
		"""Remove last value from stack"""
		
		self.stack.pop()
	
	def do_rm_from_loop_stack(self):
		"""Remove first value from the loop stack"""
		
		self.loop_list[0] = self.stack.pop()
	
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
		
		word = def_stack[0]
		word_body = def_stack[1:]
		new_word = word_body[0]
		if len(word_body) > 1:
			for w in word_body[1:]:
				new_word += " "+w
		
		self.words[word] = lambda: self.execute_string(new_word, custom_word=True)
	
	def execute_list(self, words):
		"""Execute Farth code from list like ['1', '2', '3']"""
		
		string = words[0]
		if len(words) > 0:
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
			
			if len(word) == 0: # If word is empty
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
					
					if self.stack.pop() == 1:
						self.execute_list(body)
					else:
						if len(else_body) > 0:
							self.execute_list(else_body)
			elif self.loop_n > 0 and word == LOOP:
				if self.loop_list[0] == 1:
					pos = self.loop_list[1]
					i = keys.index(pos)
					if not isWord:
						self.pos = pos
						self.i = i
				else:
					del self.loop_list[1]
					del self.loop_list[0]
			elif word[0] in '0123456789"':
				self.stack.append(eval(word))
			elif word == IF:
				self.if_n += 1
				self.if_list.append([])
				self.if_list.append([])
			elif word == DEF_WORD:
				self.def_n += 1
			elif word == DO:
				self.loop_list.append(self.stack.pop())
				self.loop_list.append(keys[keys.index(pos)+1])
				self.loop_n += 1
			else:
				func = self.words[word]
				argcount = func.__code__.co_argcount # Get argument count
				if ismethod(func):
					argcount -= 1
				
				if argcount > 0:
					res = func(*self.stack[-argcount:])
					self.stack = self.stack[0:-argcount]
				else:
					res = func()
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
