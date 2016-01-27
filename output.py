#!/usr/bin/env python3

from flask import Flask, request, session
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
    d = request.form['data']
    with open('subin','a') as f:
        f.write(d)    
        
    kill_task()
    pid = os.fork()
    if pid == 0:
        os.system('./redirect_in/in tmp')
    else:
        return ''

def get_out():
    result = ''
    with open('subout','rb') as f:
        result = f.read()
    return result

@app.route('/getout', methods=['GET'])
def getout_GET():
    return get_out()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port=81,host='0.0.0.0')
