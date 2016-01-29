#!/usr/bin/env python3

from flask import Flask, request, session
import os
from jinja2 import Environment, FileSystemLoader
import elf
import codecs
import stat
import config

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

    funcs = config.get_funcs()
    api32e = funcs['32']
    api32n = config.get_api_name(32)
    for i in api32n:
        if i in api32e:
            api32n.remove(i)

    api64e = funcs['64']
    api64n = config.get_api_name(64)
    for i in api64n:
        if i in api64e:
            api64n.remove(i)

    return template.render(header=result,sections=ss,programs=ps,apis32e=api32e,apis64e=api64e,apis32n=api32n,apis64n=api64n)

@app.route('/inf', methods=['POST'])
def inf_POST():
    return request.form['data']

def get_cmd():
    return ' '.join([cwd+'tracer/tracer'+session['class'],session['ro_addr'],session['ro_size'],'tmp'])

@app.route('/start', methods=['GET'])
def start_GET():
    pid = os.fork()
    if pid == 0:
        elf.trace_elf(get_cmd())
    else:
        return ''

def kill_task():
    elf.kill_by_comm('tracer32', 14)
    elf.kill_by_comm('tracer64', 14)

@app.route('/input', methods=['POST'])
def input_GET():
    d = request.form['data']
    with open('subin','ab') as f:
        f.write(d)

    kill_task()
    pid = os.fork()
    if pid == 0:
        elf.trace_elf(get_cmd())
    else:
        return ''

@app.route('/stop', methods=['GET'])
def stop_GET():
    kill_task()
    return ''

def get_out():
    result = ''
    with open('out','rb') as f:
        result = f.read()
    return result

@app.route('/getout', methods=['GET'])
def getout_GET():
    return get_out()
            
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port=80,host='0.0.0.0')
