#!/usr/bin/env python3

from flask import Flask
import os

app = Flask(__name__)
img = 'debian07'

@app.route('/', methods=['GET'])
def home_POST():
    os.system('docker kill $(docker ps -a -q) && docker rm $(docker ps -a -q)')
    os.system('docker run -d -p 80:80 '+img+' ./root/trace/app.py')
    os.system('docker run -d -p 81:81 '+img+' ./root/trace/output.py')

    return '<script>window.location.port=80</script>'
	
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(port=90,host='0.0.0.0')
