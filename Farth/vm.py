#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Farth.funcs import StackUnderflow, FarthError
from sys import getsizeof

class FarthVM(object):
	def __init__(self, program, farth):
		if program:
			self.program = [line.split(" ") for line in program.split("\n")]
		else:
			self.program = []
		self.pc = 0
		self.stack = []
		# Stack for defining words
		self.def_stack = []
		self.def_n = 0
		# Stack for if-else statements
		self.if_list = [[], []]
		self.if_n = 0
		self.else_n = 0
		# Loop stack
		self.loop_list = []
		self.loop_n = 0
		
		self.farth = farth
		
		self.bytes = {"\x01": "eword", "\x02": "push",
			"\x03": "pop", "\x04": "add",
			"\x05": "sub", "\x06": "mul",
			"\x07": "div", "\x08": "mod",
			"\x09": "nop", "\x10": "include",
			"\x11": "lt", "\x12": "gt",
			"\x13": "eq", "\x14": "neq",
			"\x15": "lteq", "\x16": "gteq",
			"\x17": "dup", "\x18": "swap",
			"\x19": "rot", "\x20": "over",
			"\x21": "2dup", "\x22": "2swap",
			"\x23": "2drop", "\x24": "2rot",
			"\x25": "2over", "\x26": "ifninc",
			"\x27": "ifndec", "\x28": "elsenset",
			"\x29": "elsenz", "\x30": "checkif",
			"\x31": "iflistadd", "\x32": "elselistadd",
			"\x33": "clearif", "\x34": "defninc",
			"\x35": "defndec", "\x36": "defpush",
			"\x37": "enddef", "\x38": "cleardef",
			"\x39": "loopndec", "\x40": "loopninc",
			"\x41": "looppush", "\x42": "addtols",
			"\x43": "loop", "\x44": "cpfls",
			"\x45": "revstack", "\x46": "printstack",
			"\x47": "print", "\x48": "stri",
			"\x49": "slice", "\x50": "strlen",
			"\x51": "strrev", "\x52": "sizeof",
			"\x53": "tostr", "\x54": "upper",
			"\x55": "lower", "\x56": "forget",
			"\x57": "dis", "\x58": "halt"}
	
	def def_word(self, def_stack):
		"""Define new word"""
		
		try:
			word = def_stack[0]
		except IndexError:
			raise FarthError(self, "Word definition is empty")
		word_body = def_stack[1:]
		for i in range(len(word_body)):
			if len(word_body[i]) > 1:
				word_body[i][1:] = ["%s" %arg for arg in word_body[i][1:]]
		
		self.farth.words[word] = lambda vm: vm.execute_code(word_body)
	
	def execute_code(self, code):
		"""Silently execute VM code"""
		
		for i in code:
			args = [eval(arg) for arg in i[1:]] if len(i) > 1 else []
			i[0] = i[0].lower()
			getattr(self, "i_"+i[0])(*args)
	
	def i_eword(self, word):
		"""An instruction to expand word"""
		
		try:
			self.farth.words[word](self)
		except KeyError:
			raise FarthError(self.farth, "Unknown word")
	
	def i_push(self, a):
		"""Push value onto the stack"""
		
		self.stack.append(a)
	
	def i_pop(self):
		"""Remove value from the stack"""
		
		try:
			self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_add(self):
		"""Addition"""
		
		try:
			self.stack.append(self.stack.pop() + self.stack.pop())
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_sub(self):
		"""Subtraction"""
		
		try:
			self.stack.append(self.stack.pop() - self.stack.pop())
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_mul(self):
		"""Multiplication"""
		
		try:
			self.stack.append(self.stack.pop() * self.stack.pop())
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_div(self):
		"""Division"""
		
		try:
			self.stack.append(float(self.stack.pop()) / self.stack.pop())
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_mod(self):
		"""Modulo"""
		
		try:
			self.stack.append(self.stack.pop() % self.stack.pop())
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_nop(self):
		"""Do nothing"""
		
		pass
	
	def i_include(self):
		"""Include code from file"""
		
		try:
			filename = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		try:
			f = open(eval(filename))
		except IOError:
			raise FarthError(self.farth, "Failed to open '%s'" %filename)
		code = f.read()
		f.close()
		self.farth.compile_and_execute(code)

	
	def i_lt(self):
		"""Check if first value is smaller than second
		(Remember rules of stack)"""
		
		try:
			o1 = self.stack.pop()
			o2 = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(1 if o1 < o2 else 0)
	
	def i_gt(self):
		"""Check if first value is greater than second
		(Remember rules of stack)"""
		
		try:
			o1 = self.stack.pop()
			o2 = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(1 if o1 > o2 else 0)
	
	def i_eq(self):
		"""Check if first value is equal to second
		(Remember rules of stack)"""
		
		try:
			o1 = self.stack.pop()
			o2 = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(1 if o1 == o2 else 0)
	
	def i_neq(self):
		"""Check if first value is not equal to second
		(Remember rules of stack)"""
		
		try:
			o1 = self.stack.pop()
			o2 = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(1 if o1 != o2 else 0)
	
	def i_gteq(self):
		"""Check if first value is greater or equal than second
		(Remember rules of stack)"""
		
		try:
			o1 = self.stack.pop()
			o2 = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(1 if o1 >= o2 else 0)
	
	def i_lteq(self):
		"""Check if first value is less or equal than second
		(Remember rules of stack)"""
		
		try:
			o1 = self.stack.pop()
			o2 = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(1 if o1 <= o2 else 0)
	
	def i_dup(self):
		"""Duplicate value"""
		
		try:
			self.stack.append(self.stack[-1])
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_rot(self):
		"""'Rotate' values"""
		
		try:
			self.stack = self.stack[1:] + self.stack[:1]
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_over(self):
		"""Add previous value to the stack"""
		
		try:
			n = self.stack[-2]
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack.append(n)
	
	def i_swap(self):
		"""Swap values"""
		
		try:
			n1, n2 = self.stack[-1], self.stack[-2]
			self.stack[-1], self.stack[-2] = n2, n1
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_2dup(self):
		"""Duplicate pair of values"""
		
		try:
			self.stack.append(self.stack[-2])
			self.stack.append(self.stack[-1])
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_2drop(self):
		"""Remove last pair of items"""
		
		try:
			self.stack.pop()
			self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_2over(self):
		"""Add previous pair of values to the stack"""
		
		try:
			d = [self.stack[-3], self.stack[-4]]
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.stack += d
	
	def i_2swap(self):
		"""Swap 2 pairs of values"""
		
		try:
			n1, n2, n3, n4 = self.stack[-1], self.stack[-2], \
			self.stack[-3], self.stack[-4]
			
			self.stack[-1], self.stack[-2], self.stack[-3], self.stack[-4] = \
			n3, n4, n1, n2
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_2rot(self):
		"""'Rotate' pairs of values"""
		
		try:
			self.stack = self.stack[2:] + self.stack[:2]
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_ifninc(self):
		"""Increment if-counter"""
		
		self.if_n += 1
	
	def i_ifndec(self):
		"""Decrement if-counter"""
		
		self.if_n -= 1
	
	def i_elsenset(self):
		"""Start adding words to else_list"""
		
		if self.if_n == 1:
			self.else_n = 1
	
	def i_elsenz(self):
		"""Stop adding words to else_list"""
		
		self.else_n = 0
	
	def i_iflistadd(self, word):
		"""Add word to the list that will be executed if condition if true"""
		
		self.if_list[0].append(word)
	
	def i_elselistadd(self, word):
		"""Add word to the list that will be executed if condition if false"""
		
		self.if_list[1].append(word)
	
	def i_clearif(self):
		"""Clear if_list"""
		
		self.if_list = [[], []]
	
	def i_checkif(self):
		"""Check condition and execute code depending on condition"""
		
		if self.if_n > 0:
			self.i_ifndec()
			self.i_elsenz()
			
			try:
				v = self.stack.pop()
			except IndexError:
				raise StackUnderflow(self.farth)
			
			if v == 1:
				for i in self.if_list[0]:
					getattr(self, "i_"+i[0].lower())(*i[1:])
			else:
				for i in self.if_list[1]:
					getattr(self, "i_"+i[0].lower())(*i[1:])
			
			if self.if_n == 0:
				self.i_clearif()
	
	def i_defninc(self):
		"""Increment definition count"""
		
		self.def_n += 1
	
	def i_defndec(self):
		"""Decrement definition count"""
		
		self.def_n -= 1
	
	def i_defpush(self, word):
		"""Push word to definition stack"""
		
		self.def_stack.append(word)
	
	def i_enddef(self):
		"""End definition and define word"""
		
		if self.def_n > 0:
			self.i_defndec()
			if self.def_n == 0:
				self.def_word(self.def_stack)
				self.i_cleardef()
	
	def i_cleardef(self):
		"""Clear definition stack"""
		
		self.def_stack = []
	
	def i_loopndec(self):
		"""Decrement loop count"""
		
		self.loop_n -= 1
	
	def i_loopninc(self):
		"""Increment loop count"""
		
		self.loop_n += 1
	
	def i_looppush(self):
		"""Add to loop stack number and current position"""
		
		try:
			self.loop_list.append([self.stack.pop(), self.pc])
		except IndexError:
			raise StackUnderflow(self.farth)
		
		self.i_loopninc()
	
	def i_addtols(self):
		"""Add to loop stack"""
		
		try:
			self.loop_list[-1][0] = self.stack.pop()
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_loop(self):
		"""Start loop"""
		
		if self.loop_list[self.loop_n-1][0] > 1:
			self.loop_list[self.loop_n-1][0] -= 1
			self.pc = self.loop_list[self.loop_n-1][1]
		else:
			del self.loop_list[self.loop_n-1]
			self.loop_n -= 1
	
	def i_cpfls(self):
		"""Copy value from loop stack to the data stack"""
		
		self.stack.append(self.loop_list[-1][0])
	
	def i_revstack(self):
		"""Reverse stack"""
		
		try:
			self.stack = self.stack[::-1]
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_printstack(self):
		"""Print stack contents"""
		
		print(self.stack)
	
	def i_print(self):
		"""Print value from the stack"""
		
		try:
			print(eval(self.stack.pop()))
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_stri(self):
		"""str[index]"""
		
		try:
			index = self.stack.pop()
			if type(index) is not int and type(index) is not float:
				raise FarthError(self.farth, "Index must be a number")
			s = self.stack.pop()
			if type(s) is not str:
				raise FarthError(self.farth, "Attempt to use 'stri' on non-string")
			if len(s)-1 < int(index):
				raise FarthError(self.farth, "String is too short")
			self.stack.append(s[int(index)])
		except IndexError:
			raise StackUnderflow(vm.farth)
	
	def i_slice(self):
		"""Slices string"""
		
		try:
			index2 = self.stack.pop()
			index1 = self.stack.pop()
			if type(index1) is not int and type(index1) is not float and \
				type(index2) is not int and type(index2) is not float:
				raise FarthError(self.farth, "Index must be a number")
			s = self.stack.pop()
			if type(s) is not str:
				raise FarthError(self.farth, "Attempt to use 'slice' on non-string")
			if len(s)-1 < int(index1):
				raise FarthError(self.farth, "String is too short")
			self.stack.append(s[int(index1):int(index2)])
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_strlen():
		"""Get string length"""
		
		try:
			s = self.stack.pop()
			if type(s) is not str:
				raise FarthError(self.farth, "%s is not a string" %s)
			self.stack.append(len(s))
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_strrev(self):
		"""Reverse string"""
		
		try:
			s = self.stack.pop()
			if type(s) is not str:
				raise FarthError(self.farth, "%s is not a string" %s)
			self.stack.append(s[::-1])
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_sizeof(self):
		"""Get size of value"""
		
		try:
			self.stack.append(getsizeof(self.stack.pop()))
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_tostr(self):
		"""Convert number to string"""
		
		try:
			self.stack[-1] = str(self.stack[-1])
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_upper(self):
		"""Convert string to uppercase"""
		
		try:
			if type(self.stack[-1]) is str:
				self.stack[-1] = self.stack[-1].upper()
			else:
				raise FarthError(self.farth, "%s is not a string" %s)
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_lower(self):
		"""Convert string to lowercase"""
		
		try:
			if type(self.stack[-1]) is str:
				self.stack[-1] = self.stack[-1].lower()
			else:
				raise FarthError(self.farth,
					"%s is not a string" %self.stack[-1])
		except IndexError:
			raise StackUnderflow(self.farth)
	
	def i_forget(self):
		"""Remove word from dictionary"""
		
		try:
			word = self.stack.pop()
			self.farth.words.pop(eval(word))
		except IndexError:
			raise StackUnderflow(self.farth)
		except KeyError:
			raise FarthError(self.farth, "word '%s' is not defined" %word)
	
	def i_dis(self):
		"""Print VM code"""
		
		print (self.gen_string())
	
	def i_halt(self):
		"""Stop execution"""
		
		self.pc = None
	
	def gen_string(self):
		"""Get VM code as string"""
		
		string = ''
		
		for i in self.program:
			for j in i:
				string += j
				string += " "
			string = string[0:-1]
			string += "\n"
		
		return string[0:-1]
	
	def step(self):
		i = self.program[self.pc]
		args = [eval(arg) for arg in i[1:]] if len(i) > 1 else []
		i = i[0:1] + args
		
		self.pc += 1
		if self.if_n > 0 and (self.if_n > 1 or i[0].lower() \
		not in ["elsenset", "checkif", "ifninc"]):
				if i[0].lower() == "checkif" and self.if_n > 1:
					self.if_n -= 1
				if self.else_n == 1:
					self.if_list[1].append(i)
				else:
					self.if_list[0].append(i)
		elif self.def_n > 0 and (i[0].lower() != "enddef" or self.def_n > 1):
				if i[0].lower() == "enddef":
					self.def_n -= 1
					self.def_stack.append(i)
				elif i[0].lower() == "defpush" and self.def_n == 1:
					self.i_defpush(i[1])
				else:
					self.def_stack.append(i)
		else:
			getattr(self,
				"i_" + i[0].lower())(*args)
	
	def execute(self):
		while self.pc is not None:
			if self.pc >= len(self.program):
				break
			self.step()
