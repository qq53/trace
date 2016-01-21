from flask import Flask, request, session
import os
import elf

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd+'templates'))

@app.route('/start', methods=['GET'])
def start_GET():
    os.system('./redirect_in/in ./tmp')
    return ''

@app.route('/stop', methods=['GET'])
def stop_GET():
    elf.kill_by_comm('in')
    return ''

def get_out():
    with open('subout','r') as f:
        return f.readlines()

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
