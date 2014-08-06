#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from xml.dom import minidom
from manage_project.dependencies import add, remove
from manage_project.change_lang import change_lang
from manage_project.change_name import rename
from manage_project.change_authors import change_author
from manage_project.change_description import change_description
from manage_project.change_version import change_version
from manage_project.change_date import update_date
import config
name=minidom.parse("project.xml").getElementsByTagName("name")[0].childNodes[0].nodeValue.strip()
full_path=os.path.realpath(__file__)
full_path=full_path[0:full_path.rindex(os.path.sep)]
try:
	arg1 = sys.argv[1].lower()
except IndexError:
	exit(0)
if arg1 in ["rename"]:
	rename(full_path, sys.argv[2])
elif arg1 in ["change_lang", "change_language"]:
	change_lang(full_path, sys.argv[2])
elif arg1 in ["change_authors", "change_auth"]:
	change_author(full_path, sys.argv[2])
elif arg1 in ["change_descr", "change_description"]:
	change_description(full_path , sys.argv[2])
elif arg1 in ["change_ver", "change_version"]:
	change_version(full_path, sys.argv[2])
elif arg1 in ["update_date"]:
	update_date(full_path)
elif arg1 in ["dependencies"]:
	if sys.argv[2].lower() in ["add"]:
		add(full_path, sys.argv[3])
	elif sys.argv[2].lower() in ["remove", "rm"]:
		remove(full_path, sys.argv[3])
elif arg1 in ["compile"]:
	import py_compile, distutils.core
	
	n=config.directories_to_compile
	for n1 in n:
		py_files = os.listdir(full_path+os.path.sep+n1)
		for py_file in py_files:
			if py_file.endswith(".py"):
				py_compile.compile(full_path+os.path.sep+n1+os.path.sep+py_file)
		if os.path.exists(full_path+os.path.sep+n1+os.path.sep+"__pycache__"):
			distutils.dir_util.copy_tree(full_path+os.path.sep+n1+os.path.sep+"__pycache__", full_path+os.path.sep+"bin")
			distutils.dir_util.remove_tree(full_path+os.path.sep+n1+os.path.sep+"__pycache__")
		else:
			pyc_files = os.listdir(full_path+os.path.sep+n1)
			for pyc_file in pyc_files:
				if pyc_file.endswith(".pyc"):
					os.rename(full_path+os.path.sep+n1+os.path.sep+pyc_file, full_path+os.path.sep+"bin"+os.path.sep+pyc_file)