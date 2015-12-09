#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask
import os

app = Flask(__name__)
		
@app.route('/', methods=['GET'])
def home_POST():
    os.system('docker kill $(docker ps -a -q) && docker rm $(docker ps -a -q)')
    os.system('docker run -d -p 80:80 debian06 ./root/trace/app.py')

    return '<script>window.location.port=80</script>'
	
if __name__ == '__main__':
	app.run(port=90,host='0.0.0.0')
