#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from jinja2 import Environment, FileSystemLoader
import os
import codecs

def make():
	cwd = os.path.split(os.path.realpath(__file__))[0] + '/'

	env = Environment(loader = FileSystemLoader(cwd+'templates'))
	template_index = env.get_template('index.html')
	
	with codecs.open(cwd+'index.html', 'w', 'utf-8') as f:
		f.write(template_index.render())

if __name__ == '__main__':
	make()
