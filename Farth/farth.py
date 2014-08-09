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

def do_i():
	global stack
	stack.append(loop_list[-1][0])

def equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left == right else 0)

def do_include(filename):
	f = open(filename)
	code = f.read()
	f.close()
	execute_string(code)

def remove_from_stack():
	global stack
	stack.pop()

def do_l():
	global loop_list, loop_n, stack
	loop_list[0] = stack.pop()

words = {"def": [6, do_pass],
	";": [7, do_pass],
	"+": [8, lambda x, y: x+y], " ": [19, do_pass],
	"-": [20, lambda x, y: x-y], "*": [21, lambda x, y: x*y],
	"/": [22, lambda x, y: float(x)/float(y)],
	"%": [23, lambda x, y: x%y], ".": [24, remove_from_stack],
	"print": [29, do_print], "do": [30, do_pass],
	"dup": [25, dup], "if": [26, do_pass], "loop": [31, do_pass],
	"=": [27, equal], "endif": [28, do_pass], "include": [32, do_include],
	".l": [33, do_l], "i": [34, do_i], "else": [35, do_pass]}

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

def find_words(s, word=words):
	found_words = {}
	lines = s.split("\n")
	for i in range(len(lines)):
		words_ = re.findall(r'(".*?"|[^ ]+)', lines[i])
		j = 1
		for word in words_:
			found_words[(i+1, j)] = word
			j += len(word) + 1
	
	return found_words

def get_newid():
	max_ = 0
	for word in words:
		max_ = max(words[word][0], max_)
	
	return max_

def def_word(def_stack):
	global words
	word = def_stack[0]
	word_body = def_stack[1:]
	new_word = word_body[0]
	if len(word_body) > 1:
		for w in word_body[1:]:
			new_word += " "+w
	print("New word: %s %s" %(word, new_word))
	words[word] = [get_newid(), lambda: execute_string(new_word)]

def execute_list(words):
	string = words[0]
	if len(words) > 0:
		for word in words[1:]:
			string += " " + word
	
	execute_string(string)

def execute(found_words):
	global stack
	global def_stack
	global def_n
	global if_n
	global if_list, else_n
	global loop_list
	global loop_n
	global pos, i
	
	keys = sorted(list(found_words.keys()))
	
	while i < len(keys):
		pos = keys[i]
		word = found_words[pos]
		i += 1
		
		if len(word) == 0: # If word is empty
			continue
		elif def_n > 0:
			if word != ";" or def_n > 1:
				if word == "def":
					def_n += 1
				elif word == ";":
					def_n -= 1
				def_stack.append(word)
			else:
				def_n -= 1
				if def_n < 1:
					def_word(def_stack)
					def_stack = []
		elif if_n > 0:
			if word == "else" and if_n == 1:
				else_n = 1
			elif else_n == 1 and (word != "endif" or if_n > 1):
				if word == "endif":
					if_n -= 1
				elif word == "if":
					if_n += 1
				if_list[1].append(word)
			elif word != "endif" or if_n > 1: # endif
				if word == "if":
					if_n += 1
				elif word == "endif":
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
		elif loop_n > 0 and word == "loop": # loop
			if loop_list[0] == 1:
				pos = loop_list[1]
				i = keys.index(pos)
			else:
				del loop_list[1]
				del loop_list[0]
		elif word[0] in '0123456789"':
			stack.append(eval(word))
		elif word == "if": # if
			if_n += 1
			if_list.append([])
			if_list.append([])
		elif word in words and words[word][0] == 6: # def
			def_n += 1
		elif word in words and words[word][0] == 30: # do
			loop_list.append(stack.pop())
			loop_list.append(keys[keys.index(pos)+1])
			loop_n += 1
		else:
			if word in stack:
				stack.remove(word)
			func = words[word][1]
			argcount = func.__code__.co_argcount # Get argument count
			if argcount > 0:
				res = func(*stack[-argcount:])
				stack = stack[0:-argcount]
			else:
				res = func()
			if res is not None:
				stack.append(res)

def execute_string(s):
	global code, code_str
	code_str += s+"\n"
	found_words = find_words(code_str, words)
	code.update(found_words)
	execute(code)
