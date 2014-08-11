#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

v = "0.3.5"

setup(name="Farth",
	version=v,
	author="Ivan Konovalov",
	author_email="rvan.mega@gmail.com",
	description="Farth - is an attempt to implement Forth",
	packages=["Farth"],
	url="https://github.com/SPython/farth",
	download_url="https://github.com/SPython/farth/tarball/"+v,
	keywords=["forth", "implementation", "language"])
