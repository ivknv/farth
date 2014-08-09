#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.06 16:21 +0600

Farth - an attempt to implement Forth
"""

import re

def do_pass():
	pass

def do_print(s):
	print(s)

def dup():
	global stack
	stack.append(stack[-1])

def do_cp_from_loop_stack():
	global stack
	stack.append(loop_list[-1][0])

def equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left == right else 0)

def not_equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left != right else 0)

def less_or_equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left <= right else 0)

def greater_or_equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left >= right else 0)

def do_include(filename):
	f = open(filename)
	code = f.read()
	f.close()
	execute_string(code)

def remove_from_stack():
	global stack
	stack.pop()

def do_rm_from_loop_stack():
	global loop_list, loop_n, stack
	loop_list[0] = stack.pop()

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

words = {DEF_WORD: do_pass,
	END_DEF_WORD: do_pass,
	PLUS: lambda x, y: x+y,
	MINUS: lambda x, y: x-y, MUL: lambda x, y: x*y,
	DIV: lambda x, y: float(x)/float(y),
	MODULO: lambda x, y: x%y, RM: remove_from_stack,
	PRINT: do_print, DO: do_pass,
	DUP: dup, IF: do_pass, LOOP: do_pass,
	EQUAL: equal, NOT_EQUAL: not_equal,
	LESS_OR_EQUAL: less_or_equal, GREATER_OR_EQUAL: greater_or_equal,
	ENDIF: do_pass, INCLUDE: do_include,
	RM_FROM_LOOP_STACK: do_rm_from_loop_stack,
	CP_FROM_LOOP_STACK: do_cp_from_loop_stack, ELSE: do_pass}

stack = []
def_stack = []
def_n = 0
if_list = []
if_n = 0
else_n = 0
loop_list = []
loop_n = 0
code = []
pos = (1, 1)
i = 0
code = {}
code_str = ""

def find_words(s):
	found_words = {}
	lines = s.split("\n")
	for i in range(len(lines)):
		words_ = re.findall(r'(".*?"|[^ ]+)', lines[i])
		j = 1
		for word in words_:
			found_words[(i+1, j)] = word
			j += len(word) + 1
	
	return found_words

def def_word(def_stack):
	global words
	word = def_stack[0]
	word_body = def_stack[1:]
	new_word = word_body[0]
	if len(word_body) > 1:
		for w in word_body[1:]:
			new_word += " "+w
	
	def f():
		global i, pos, code, code_str
		i_before = i
		pos_before = pos
		code_before = code
		code_str_before = code_str
		execute_string(new_word, custom_func=True)
		i = i_before
		pos = pos_before
		code = code_before
		code_str = code_str_before
	
	words[word] = f

def execute_list(words):
	string = words[0]
	if len(words) > 0:
		for word in words[1:]:
			string += " " + word
	
	execute_string(string)

def debug():
	print("================")
	print("stack length: %d" %len(stack))
	print("code: %s" %code)
	print("def_n: %d" %def_n)
	print("def_stack length: %d" %len(def_stack))
	print("if_n: %d" %if_n)
	print("if_list length: %d" %len(if_list))
	print("loop_n: %d" %loop_n)
	print("loop_list length: %d" %len(loop_list))
	print("pos: %d:%d" %(pos[0], pos[1]))
	print("i: %d" %i)
	input(">>> ")
	print("================")

def execute(found_words, isWord=False):
	global stack
	global def_stack
	global def_n
	global if_n
	global if_list, else_n
	global loop_list
	global loop_n
	if not isWord:
		global pos, i
	else:
		pos = (1, 1)
		i = 0
	
	keys = sorted(list(found_words.keys()))
	
	while i < len(keys):
		pos = keys[i]
		word = found_words[pos]
		i += 1
		
		if len(word) == 0: # If word is empty
			continue
		elif def_n > 0:
			if word != END_DEF_WORD or def_n > 1:
				if word == DEF_WORD:
					def_n += 1
				elif word == END_DEF_WORD:
					def_n -= 1
				def_stack.append(word)
			else:
				def_n -= 1
				if def_n < 1:
					def_word(def_stack)
					def_stack = []
		elif if_n > 0:
			if word == ELSE and if_n == 1:
				else_n = 1
			elif else_n == 1 and (word != ENDIF or if_n > 1):
				if word == ENDIF:
					if_n -= 1
				elif word == IF:
					if_n += 1
				if_list[1].append(word)
			elif word != ENDIF or if_n > 1:
				if word == IF:
					if_n += 1
				elif word == ENDIF:
					if_n -= 1
				if_list[0].append(word)
			else:
				body = if_list[0]
				else_body = if_list[1]
				if_list[0], if_list[1] = [], []
				if_n -= 1
				else_n -= 1
				
				if stack.pop() == 1:
					execute_list(body)
				else:
					if len(else_body) > 0:
						execute_list(else_body)
		elif loop_n > 0 and word == LOOP:
			if loop_list[0] == 1:
				pos = loop_list[1]
				i = keys.index(pos)
			else:
				del loop_list[1]
				del loop_list[0]
		elif word[0] in '0123456789"':
			stack.append(eval(word))
		elif word == IF:
			if_n += 1
			if_list.append([])
			if_list.append([])
		elif word == DEF_WORD:
			def_n += 1
		elif word == DO:
			loop_list.append(stack.pop())
			loop_list.append(keys[keys.index(pos)+1])
			loop_n += 1
		else:
			func = words[word]
			argcount = func.__code__.co_argcount # Get argument count
			
			if argcount > 0:
				res = func(*stack[-argcount:])
				stack = stack[0:-argcount]
			else:
				res = func()
			if res is not None:
				stack.append(res)

def execute_string(s, add_newline=False, custom_func=False):
	global code, code_str
	if not custom_func:
		code_str += s + " "
		if add_newline:
			code_str += "\n"
		found_words = find_words(code_str)
		code.update(found_words)
		execute(code)
	else:
		found_words = find_words(s)
		execute(found_words, isWord=True)
