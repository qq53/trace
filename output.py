#!/usr/bin/env python3

from flask import Flask, request
import os
import elf
import stat

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
os.chdir(cwd)

@app.route('/', methods=['POST'])
def home_POST():
    f = request.files['fileToUpload']
    sf = cwd+'tmp'

    f.save(sf)
    os.chmod(sf,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    return ''

@app.route('/start', methods=['GET'])
def start_GET():
    elf.rm('subout')
    pid = os.fork()
    if pid == 0:
        os.system('./redirect_in/in tmp')
        return ''
    else:
        return ''

def kill_task():
    elf.kill_by_comm('in')
    elf.kill_by_comm('tmp')

@app.route('/input', methods=['POST'])
def input_POST():
    kill_task()
    d = request.form['data']
    with open('subin','w') as f:
        f.write(d)    
    elf.rm('subout')

    pid = os.fork()
    if pid == 0:
        os.system('./redirect_in/in tmp')
        return ''
    else:
        return ''

def get_out(n):
    result = ''
    with open('subout','r') as f:
        d = f.readlines()
    if n < len(d):
        result = ''.join(d[n:])
    else:
        kill_task()

    return result

@app.route('/getout', methods=['GET'])
def getout_GET():
    n = request.args.get('n')
    return get_out(int(n))

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(port=81,host='0.0.0.0',debug=False)
