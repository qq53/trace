#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request
import codecs, time, json
from urllib.parse import quote
import os
from jinja2 import Environment, FileSystemLoader
from werkzeug.utils import secure_filename
import sys
from elf import elf

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd))

@app.route('/', methods=['GET'])
def home():
	with codecs.open(cwd+'index.html','r','utf-8') as f:
		d = f.read()
		return d
		
@app.route('/', methods=['POST'])
def home_POST():
	f = request.files['fileToUpload']
	f.save('tmp')
	#fname = secure_filename(f.filename)
	
	return elf('tmp')

if __name__ == '__main__':
    app.run(port=80,host='0.0.0.0')
