#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

import os, time

def elf(tmpf):
	return 'ELF'
	fn = str(int(time.time()))
	os.system("file " + tmpf + " | awk -F ': ' {'print $2'} > "+fn)
	fs = open(fn, 'r') 
	ftype = fs.read()
	fs.close()
	if ftype[:3] == 'ELF':
		os.system("readelf -a " + tmpf + " > "+fn)
		fs = open(fn, 'r') 
		elf_inf = fs.read()
		fs.close()
		result = elf_inf
	else:
		result = 'not elf'

	os.remove(tmpf)
	os.remove(fn)
	return result
