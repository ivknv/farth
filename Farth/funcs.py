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
			obj.code_str.split("\n")[obj.pos[0]-1],
			get_current_word(obj))
		
		msg = "%s at %d:%d:\n%s" %(message, obj.pos[0], obj.pos[1],
			code_fragment)
		super(FarthError, self).__init__(msg)

class StackUnderflow(FarthError):
	def __init__(self, obj):
		super(StackUnderflow, self).__init__(obj, "Stack underflow")

class Funcs(object):
	@staticmethod
	def do_plus(vm):
		vm.program.append(["ADD"])
	
	@staticmethod
	def do_minus(vm):
		vm.program.append(["SUB"])
	
	@staticmethod
	def do_mul(vm):
		vm.program.append(["MUL"])
	
	@staticmethod
	def do_div(vm):
		vm.program.append(["DIV"])
	
	@staticmethod
	def do_modulo(vm):
		vm.program.append(["MOD"])
	
	@staticmethod
	def do_pass(vm):
		"""Do nothing. This function mostly used as a stub."""
		
		vm.program.append(["NOP"])
	
	@staticmethod
	def do_print(vm):
		"""Print last value in stack"""
		
		vm.program.append(["PRINT"])
	
	@staticmethod
	def dup(vm):
		"""Duplicate last value in stack"""
		
		vm.program.append(["DUP"])
	
	@staticmethod
	def do_cp_from_loop_stack(vm):
		"""Copy value from loop stack"""
		
		vm.program.append(["CPFLS"])
	
	@staticmethod
	def equal(vm):
		"""=="""
		
		vm.program.append(["EQ"])
	
	@staticmethod
	def not_equal(vm):
		"""!="""
		
		vm.append(["NEQ"])
	
	@staticmethod
	def less_or_equal(vm):
		"""<="""
		
		vm.append(["LEQ"])
	
	@staticmethod
	def greater_or_equal(vm):
		""">="""
		
		vm.program.append(["GEQ"])
			
	@staticmethod
	def greater(vm):
		""">"""
		
		vm.program.append(["GT"])
				
	@staticmethod
	def less(vm):
		""">"""
		
		vm.program.append(["LT"])
		
	@staticmethod
	def do_include(vm):
		"""Include code from file"""
		
		vm.program.append(["INCLUDE"])
	
	@staticmethod
	def dis(vm):
		vm.program.append(["DIS"])
		
	@staticmethod
	def drop(vm):
		"""Remove last value from stack"""
		
		vm.program.append(["POP"])
		
	@staticmethod
	def do_add_to_loop_stack(vm):
		"""Change last value from the loop stack"""
		
		vm.program.append(["ADDTOLS"])
	
	@staticmethod
	def do_swap(vm):
		"""Swap 2 top values on the stack
		n1 n2 -- n2 n1"""
		
		vm.program.append(["SWAP"])
		
	@staticmethod
	def do_rotate(vm):
		"""'Rotates' last 3 values
		n1 n2 n3 -- n2 n3 n1"""
		
		vm.program.append(["ROT"])
		
	@staticmethod
	def do_over(vm):
		"""Duplicates first item and puts it on top of the stack
		n1 n2 -- n1 n2 n1"""
		
		vm.program.append(["OVER"])
		
	@staticmethod
	def print_stack(vm):
		"""Prints stack content"""
		
		vm.program.append(["PRINTSTACK"])
	
	@staticmethod
	def forget(vm):
		"""Remove word from dictionary"""
		
		vm.program.append(["FORGET"])
	
	@staticmethod
	def do_2dup(vm):
		"""Duplicates last pair of values
		d -- d d"""
		
		vm.program.append(["2DUP"])
		
	@staticmethod
	def do_2swap(vm):
		"""Swaps 2 last pairs of values
		d1 d2 -- d2 d1"""
		
		vm.program.append(["2SWAP"])
	
	@staticmethod
	def do_2drop(vm):
		"""Removes last pair from stack
		d --"""
		
		vm.program.append(["2DROP"])
		
	@staticmethod
	def do_2over(vm):
		"""Duplicates first pair and puts it on stack
		d1 d2 -- d1 d2 d1"""
		
		vm.program.append(["2OVER"])
		
	@staticmethod
	def reverse_stack(vm):
		"""Reverses stack
		n1 n2 ... -- ... n2 n1"""
		
		vm.program.append(["REVSTACK"])
	
	@staticmethod
	def do_quit(vm):
		"""Stop execution"""
		
		vm.program.append(["HALT"])
	
	@staticmethod
	def do_def(vm):
		"""Start word definition"""
		
		vm.program.append(["DEFNINC"])
		vm.farth.def_just_started = True
	
	def do_enddef(vm):
		"""End word definition"""
		
		vm.program.append(["ENDDEF"])
	
	@staticmethod
	def do_else(vm):
		"""Define what to do if condition is false"""
		
		vm.program.append(["ELSENSET"])
	
	@staticmethod
	def do_if(vm):
		"""Start if statement"""
		
		vm.program.append(["IFNINC"])
	
	@staticmethod
	def do_endif(vm):
		"""End if statement"""
		
		vm.program.append(["CHECKIF"])
	
	def do_do(vm):
		"""Push value to loop stack"""
		
		vm.program.append(["LOOPPUSH"])
	
	@staticmethod
	def do_loop(vm):
		"""Start loop"""
		
		vm.program.append(["LOOP"])
	
	@staticmethod
	def lower(vm):
		"""Convert string to lowercase"""
		
		vm.program.append(["LOWER"])
	
	@staticmethod
	def upper(vm):
		"""Convert string to uppercase"""
		
		vm.program.append(["UPPER"])
	
	@staticmethod
	def to_str(vm):
		"""Convert number to string"""
		
		vm.program.append(["TOSTR"])
	
	@staticmethod
	def str_index(vm):
		"""str[index]"""
		
		vm.program.append(["STRI"])
	
	@staticmethod
	def str_slice(vm):
		"""Slices string"""
		
		vm.program.append(["SLICE"])
	
	@staticmethod
	def str_len(vm):
		"""Get string length"""
		
		vm.program.append(["STRLEN"])
	
	@staticmethod
	def str_reverse(vm):
		"""Reverse string"""
		
		vm.program.append(["STRREV"])
	
	@staticmethod
	def sizeof(vm):
		"""Get size of value"""
		
		vm.program.append(["SIZEOF"])
