#!/usr/bin/env python
# -*- coding: utf-8 -*-

def do_pass():
	pass

def do_print(s):
	print(s)

def dup():
	global stack
	stack.append(stack[-1])

def do_include(filename):
	f = open(filename)
	code = f.read()
	f.close()
	execute_string(code)

def equal():
	global stack
	left = stack.pop()
	right = stack.pop()
	stack.append(1 if left == right else 0)
