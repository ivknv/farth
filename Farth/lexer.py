#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def do_pass():
	pass

def do_print(s):
	print(s)

def dup():
	global stack
	stack.append(stack[-1])

def equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left == right else 0)

words = {"def": [6, do_pass],
	";": [7, do_pass],
	"+": [8, lambda x, y: x+y], " ": [19, do_pass],
	"-": [20, lambda x, y: x-y], "*": [21, lambda x, y: x*y],
	"/": [22, lambda x, y: float(x)/float(y)],
	"%": [23, lambda x, y: x%y], ".": [24, lambda: stack.pop()],
	"print": [29, do_print],
	"dup": [25, dup], "if": [26, do_pass],
	"=": [27, equal], "endif": [28, do_pass]}

def find_words(s, word=words):
	found_words = []
	lines = s.split("\n")
	for i in range(len(lines)):
		words = re.split(r'(".*"| )', lines[i])
		j = 0
		for word in words:
			if word not in words and not word[0] in '01234567890"':
				print("Unknown word at %d:%d: %s" %(i+1, j+1, word))
			j += len(word) + 1
			if word in words:
				found_words.append((i+1, j+1, word))
	
	return found_words
