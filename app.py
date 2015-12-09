#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request
import os
from jinja2 import Environment, FileSystemLoader
from elf import elf
import codecs
import stat

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd+'templates'))

@app.route('/', methods=['GET'])
def home():
	with codecs.open(cwd+'index.html','r','utf-8') as f:
		d = f.read()
		return d
		
@app.route('/', methods=['POST'])
def home_POST():
	f = request.files['fileToUpload']
	f.save('tmp')
	#os.chmod('tmp',stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

	result = elf('tmp')

	os.remove('tmp')
	template = env.get_template('inf.html')
	ss = result['sh']
	ps = result['ph']
	pss = result['pss']
	result.pop('sh')
	result.pop('ph')
	result.pop('pss')

	return template.render(header=result,sections=ss,programs=ps,process=pss)

@app.route('/inf', methods=['POST'])
def inf_POST():
	return request.form['data']
	
if __name__ == '__main__':
	app.run(port=80,host='0.0.0.0')
