#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request, session
import os
from jinja2 import Environment, FileSystemLoader
from elf import elf
import codecs
import stat

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd+'templates'))

app.secret_key = os.urandom(24)

def rm(path):
    if os.path.isfile(path):
        os.remove(path)

@app.route('/', methods=['GET'])
def home():
    with codecs.open(cwd+'index.html','r','utf-8') as f:
        d = f.read()
        return d
		
@app.route('/', methods=['POST'])
def home_POST():
    f = request.files['fileToUpload']
    sf = cwd+'tmp'

    rm(sf)
    rm("subin")
    rm("out")

    f.save(sf)
    os.chmod(sf,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    result = elf(sf)
    template = env.get_template('inf.html')
    ss = result['sh']
    ps = result['ph']
    pss = result['pss']
    result.pop('sh')
    result.pop('ph')
    result.pop('pss')

    print('1')

    with open('out','rt') as f:
        print('2')
        session['outlines'] = len(f.readlines())

    print('3')

    return template.render(header=result,sections=ss,programs=ps,process=pss)

@app.route('/inf', methods=['POST'])
def inf_POST():
    return request.form['data']

@app.route('/syn_trace', methods=['POST'])
def syn_trace_POST():
    d = request.form['data']
    if d == '':
        return ''
    with open('subin','a') as f:
        f.write(request.form['data']+'\n')
    return session['outlines']

@app.route('/running', methods=['GET'])
def running_GET():
    l = os.popen('ps -a|egrep "tracer\d{2}"').readlines()
    if len(l) > 0:
        return True
    return False

if __name__ == '__main__':
    app.run(port=80,host='0.0.0.0')
