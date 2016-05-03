#!/usr/bin/env python3

from flask import Flask, request
import os
import elf
import stat

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'

@app.route('/', methods=['POST'])
def home_POST():
    f = request.files['fileToUpload']
    sf = cwd+'tmp'

    f.save(sf)
    os.chmod(sf,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    return ''

@app.route('/start', methods=['GET'])
def start_GET():
    pid = os.fork()
    if pid == 0:
        os.system('./redirect_in/in tmp')
    else:
        return ''

def kill_task():
    elf.kill_by_comm('in')
    elf.kill_by_comm('tmp')

@app.route('/stop', methods=['GET'])
def stop_GET():
    kill_task()
    return ''

@app.route('/input', methods=['POST'])
def input_POST():
    kill_task()
    d = request.form['data']
    with open('subin','w') as f:
        f.write(d)    
        
    pid = os.fork()
    if pid == 0:
        os.system('./redirect_in/in tmp')
    else:
        return ''

def get_out():
    result = ''
    global outLines
    l = outLines
    with open('subout','r') as f:
        d = f.readlines()
    if l < len(d):
        outLines = len(d)
        result = ''.join(d[l:])
    return result

@app.route('/getout', methods=['GET'])
def getout_GET():
    return get_out()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    outLines = 0
    app.run(port=81,host='0.0.0.0',debug=True)
