#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Ivan Konovalov
@date: 2014.08.11 15:32 +0600

Contains functions for Farth
"""


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
	def remove_from_stack(obj):
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
