#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.11 15:32 +0600

Contains functions for Farth
"""

def replace(index1, index2, s, *args, **kwargs):
	return s[:index1] + s[index1:index2].replace(*args, **kwargs) + s[index2:]

def highlight_word(index, code, word):
	return replace(index-1, index+len(word), code, word,
		"\033[91m"+word+"\033[0m", 1)

def get_current_word(obj):
	return obj.code[(obj.pos[0], obj.pos[1])]

class FarthError(Exception):
	def __init__(self, obj, message):
		code_fragment = highlight_word(obj.pos[1],
			obj.code_str.split("\n")[obj.pos[0]-1], get_current_word(obj))
		msg = "%s at %d:%d:\n%s" %(message, obj.pos[0], obj.pos[1],
			code_fragment)
		super(FarthError, self).__init__(msg)

class StackUnderflow(FarthError):
	def __init__(self, obj):
		super(StackUnderflow, self).__init__(obj, "Stack underflow")

class Funcs(object):
	@staticmethod
	def do_plus(obj):
		try:
			return obj.stack.pop()+obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_minus(obj):
		try:
			return obj.stack.pop()-obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
	@staticmethod
	def do_mul(obj):
		try:
			return obj.stack.pop()*obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_div(obj):
		try:
			return float(obj.stack.pop())/obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_modulo(obj):
		try:
			return obj.stack.pop()%obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_pass(obj):
		"""Do nothing. This function mostly used as a stub."""
		
		pass
	
	@staticmethod
	def do_print(obj):
		"""Print last value in stack"""
		
		try:
			print(obj.stack.pop())
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def dup(obj):
		"""Duplicate last value in stack"""
		
		try:
			obj.stack.append(obj.stack[-1])
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_cp_from_loop_stack(obj):
		"""Copy value from loop stack"""
		
		obj.stack.append(obj.loop_list[-1][0])
	
	@staticmethod
	def equal(obj):
		"""=="""
		
		try:
			left = obj.stack.pop()
			right = obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
		obj.stack.append(1 if left == right else 0)
	
	@staticmethod
	def not_equal(obj):
		"""!="""
		
		try:
			left = obj.stack.pop()
			right = obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
		obj.stack.append(1 if left != right else 0)
	
	@staticmethod
	def less_or_equal(obj):
		"""<="""
		
		try:
			left = obj.stack.pop()
			right = obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
		obj.stack.append(1 if left <= right else 0)
	
	@staticmethod
	def greater_or_equal(obj):
		""">="""
		
		try:
			left = obj.stack.pop()
			right = obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
		obj.stack.append(1 if left >= right else 0)
	
	@staticmethod
	def greater(obj):
		""">"""
		
		obj.stack.append(1 if obj.stack.pop() > obj.stack.pop() else 0)
	
	@staticmethod
	def less(obj):
		""">"""
		
		obj.stack.append(1 if obj.stack.pop() < obj.stack.pop() else 0)
	
	@staticmethod
	def do_include(obj, filename):
		"""Include code from file"""
		
		try:
			f = open(filename)
		except IOError:
			raise FarthError(obj, "Failed to open '%s'" %filename)
		code = f.read()
		f.close()
		obj.execute_string(code)
		
	@staticmethod
	def drop(obj):
		"""Remove last value from stack"""
		
		try:
			obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
		
	@staticmethod
	def do_add_to_loop_stack(obj):
		"""Change last value from the loop stack"""
		
		try:
			obj.loop_list[obj.loop_n-1][0] = obj.stack.pop()
		except IndexError as e:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_swap(obj):
		"""Swap 2 top values on the stack
		n1 n2 -- n2 n1"""
		
		try:
			obj.stack[-1], obj.stack[-2] = obj.stack[-2], obj.stack[-1]
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_rotate(obj):
		"""'Rotates' last 3 values
		n1 n2 n3 -- n2 n3 n1"""
		
		try:
			n1, n2, n3 = obj.stack[-1], obj.stack[-2], obj.stack[-3]
			obj.stack[-1], obj.stack[-2], obj.stack[-3] = n2, n3, n1
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_over(obj):
		"""Duplicates first item and puts it on top of the stack
		n1 n2 -- n1 n2 n1"""
		
		try:
			obj.stack.append(obj.stack[-2])
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def print_stack(obj):
		"""Prints stack content"""
		
		print(obj.stack)
	
	@staticmethod
	def forget(obj):
		"""Remove word from dictionary"""
		
		try:
			word = obj.stack.pop()
			obj.words.pop(word)
		except IndexError:
			raise StackUnderflow(obj)
		except KeyError:
			raise FarthError(obj, "word '%s' doesn't exist" %word)
	
	@staticmethod
	def do_2dup(obj):
		"""Duplicates last pair of values
		d -- d d"""
		
		try:
			d = [obj.stack[-2], obj.stack[-1]]
			obj.stack += d
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_2swap(obj):
		"""Swaps 2 last pairs of values
		d1 d2 -- d2 d1"""
		
		try:
			n1, n2 = obj.stack[-1], obj.stack[-2]
			n3, n4 = obj.stack[-3], obj.stack[-4]
			obj.stack[-1], obj.stack[-2], \
			obj.stack[-3], obj.stack[-4] = n3, n4, n1, n2
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_2drop(obj):
		"""Removes last pair from stack
		d --"""
		
		try:
			obj.stack.pop()
			obj.stack.pop()
		except IndexError:
			raise StackUnderflow(obj)
	
	@staticmethod
	def do_2over(obj):
		"""Duplicates first pair and puts it on stack
		d1 d2 -- d1 d2 d1"""
		
		try:
			d = [obj.stack[-4], obj.stack[-3]]
			obj.stack += d
		except IndexError:
			raise StackUnderflow(obj)
