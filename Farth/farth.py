#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.06 16:21 +0600

Farth - an attempt to implement Forth
"""

from Farth.lexer import *

def do_include(filename):
	f = open(filename)
	code = f.read()
	f.close()
	execute_string(code)

words["include"] = [30, do_include]

stack = []
def_stack = []
definition = False
if_stack = []
if_n = -1

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
	global definition
	global if_n
	global if_stack
	
	for i in range(len(found_words)):
		x, y, word = found_words[i]
		if len(word) == 0: # If word is empty
			continue
		elif definition:
			if words[word][0] != 7: # ;
				def_stack.append(word)
			else:
				if "def" in def_stack:
					def_stack.append(";")
				def_word(def_stack)
				def_stack = []
				definition = False
		elif if_stack:
			if words[word][0] != 28: # endif
				if_stack[if_n].append(word)
			else:
				body = if_stack[0]
				del if_stack[0]
				if_n -= 1
				
				if stack.pop() == 1:
					execute_list(body)
		elif word[0] in '0123456789"':
			stack.append(eval(word))
		elif words[word][0] == 28:
			if_stack.append([])
			if_n += 1
		elif words[word][0] == 6: # def
			definition = True
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
	found_words = find_words(s, words)
	execute(found_words)
