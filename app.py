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

def rm(path):
    if os.path.isfile(path):
        os.remove(path)

@app.route('/', methods=['GET'])
def home():
    with codecs.open(cwd+'index.html','r','utf-8') as f:
        d = f.read()
        return d
		
def flush_outlines():
    with open('out','rt') as f:
        session['outlines'].append(len(f.readlines()))

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


    session['outlines'] = []
    session['class'] = result['class']
    session['ro_addr'] = result['ro_addr']
    session['ro_size'] = result['ro_size']

    flush_outlines()

    return template.render(header=result,sections=ss,programs=ps,process=pss)

@app.route('/inf', methods=['POST'])
def inf_POST():
    return request.form['data']

def kill_tracer():
    p32 = os.popen('ps --no-header -C tracer32 -o pid').read()
    if p32 != '':
        os.system('kill -s 14 '+p32)
        return
    p64 = os.popen('ps --no-header -C tracer64 -o pid').read()
    if p64 != '':
        os.system('kill -s 14 '+p64)

@app.route('/input', methods=['POST'])
def input_POST():
    d = request.form['data']
    if d == '':
        return ''
    with open('subin','a') as f:
        f.write(request.form['data']+'\n')

    kill_tracer()
    flush_outlines()
    out = str(' '.join([cwd+'tracer/tracer'+session['class'],'tmp',session['ro_addr'],session['ro_size'],]))
    #retrace

    #return multi outputs
    return str(session['outlines'])

@app.route('/running', methods=['GET'])
def running_GET():
    l = os.popen('ps -a|egrep "tracer\d{2}"').readlines()
    if len(l) > 0:
        return True
    return False

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port=80,host='0.0.0.0')
