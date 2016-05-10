#!/usr/bin/env python3

from flask import Flask, request, session
import os
from jinja2 import Environment, FileSystemLoader
import elf
import codecs
import stat
import config
import json
import time

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd+'templates'))

@app.route('/', methods=['GET'])
def home():
    template_index = env.get_template('index.html')
    return template_index.render()

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

    session['class'] = result['class']
    session['ro_addr'] = result['ro_addr']
    session['ro_size'] = result['ro_size']
    session['outLines'] = 0

    funcs = config.get_inter_funcs()
    api32e = funcs['32']
    api32n = config.get_api_name(32)
    comm_api = []
    for i in api32n:
        if i in api32e:
            comm_api.append(i)
    for i in comm_api:
        api32n.remove(i)

    api64e = funcs['64']
    api64n = config.get_api_name(64)
    comm_api = []
    for i in api64n:
        if i in api64e:
            comm_api.append(i)
    for i in comm_api:
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
    with open('subin','a') as f:
        f.write(d)

    pid = os.fork()
    if pid == 0:
        kill_task()
        elf.trace_elf(get_cmd())
    else:
        return ''

def get_out():
    result = ''
    with open('out','r') as f:
        d = f.readlines()
        l = session['outLines']
        #l = 0
        if l < len(d):
            session['outLines'] = len(d)
            datas = []
            for r in d[l:]:
                tmpd = {}
                if r.find('=') > 0:
                    tmp = r.split('=')
                    tmpd['result'] = tmp[-1].strip()
                    args = tmp[:-1][0].strip()
                else:
                    args = r.strip()
                tmp = args.split(' ')
                func_name = tmp[0]
                if func_name[0] == '#':
                    tmpd['danger'] = True
                    func_name = func_name[1:]
                func_args = []
                for i in tmp[1:]:
                    func_args.append(i)
                tmpd['name'] = func_name
                tmpd['args'] = func_args
                datas.append(tmpd)
            t = time.strftime('%H:%M')
            template_traceout = env.get_template('traceout.html')
            result = template_traceout.render(data=datas,time=t)
        else:
            kill_task()

    return result

@app.route('/getout', methods=['GET'])
def getout_GET():
    return get_out()

@app.route('/get_args_sum', methods=['GET'])
def get_args_sum_GET():
    return json.dumps(config.get_args_sum())

@app.route('/set_config', methods=['POST'])
def set_config_POST():
    r = config.set(key='1',
        args = json.loads(request.form['args']),
        conds = json.loads(request.form['conds']),
        name = request.form['name'],
        bit = request.form['bit']
    )
    if r == False:
        return 'false'
    else:
        return 'true'

@app.route('/get_config', methods=['GET'])
def get_config_GET():
    return config.get('1')

@app.route('/refresh', methods=['GET'])
def refresh_GET():
    session['outLines'] = 0
    kill_task()
    elf.rm("subin")
    elf.rm("subout")
    elf.rm("out")
    return 'ok'

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port=80,host='0.0.0.0',debug=True)
