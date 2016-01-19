#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request, session
import os
from jinja2 import Environment, FileSystemLoader
import elf
import codecs
import stat

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd+'templates'))

def flush_outlines():
    with open('subout','rb') as f:
        session['outlines'].append(len(f.readlines()))

def get_cmd():
    return ' '.join([cwd+'tracer/tracer'+session['class'],session['ro_addr'],session['ro_size'],'tmp'])

@app.route('/', methods=['GET'])
def home():
    with codecs.open(cwd+'index.html','r','utf-8') as f:
        d = f.read()
        return d

@app.route('/', methods=['POST'])
def home_POST():
    f = request.files['fileToUpload']
    sf = cwd+'tmp'

    elf.rm(sf)
    elf.rm("subin")
    elf.rm("subout")
    elf.rm("out")

    f.save(sf)
    os.chmod(sf,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    result = elf.elf(sf)
    template = env.get_template('inf.html')
    ss = result['sh']
    ps = result['ph']
    result.pop('sh')
    result.pop('ph')

    session['outlines'] = []
    session['class'] = result['class']
    session['ro_addr'] = result['ro_addr']
    session['ro_size'] = result['ro_size']

    return template.render(header=result,sections=ss,programs=ps)

@app.route('/inf', methods=['POST'])
def inf_POST():
    return request.form['data']

@app.route('/input', methods=['POST'])
def input_POST():
    d = request.form['data']
    if d == '':
        return ''
    with open('subin','a') as f:
        f.write(request.form['data']+'\n')

    elf.kill_tracer()
    flush_outlines()
    elf.trace_elf(get_cmd())

    return ''

@app.route('/start', methods=['GET'])
def start_GET():
    pid = os.fork()
    if pid == 0:
        f = os.popen('./tracer/tracer32 tmp 0 0').read()
        print(f)
    else:
        return ''

@app.route('/stop', methods=['GET'])
def stop_GET():
    elf.kill_tracer()
    return ''

@app.route('/running', methods=['GET'])
def running_GET():
    return elf.get_trace_str()

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port=80,host='0.0.0.0')
