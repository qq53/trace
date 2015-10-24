#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request
import codecs, time, json
from urllib.parse import quote
import os
from jinja2 import Environment, FileSystemLoader

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
	return request.files['fileToUpload'].filename

if __name__ == '__main__':
    app.run(port=80)