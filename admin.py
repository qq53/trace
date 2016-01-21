from flask import Flask
import os

app = Flask(__name__)
		
@app.route('/', methods=['GET'])
def home_POST():
    os.remove('subin')
    os.remove('out')
    os.system('docker kill $(docker ps -a -q) && docker rm $(docker ps -a -q)')
    os.system('docker run -d -p 80:80 debian06 ./root/trace/app.py')

    return '<script>window.location.port=80</script>'
	
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

if __name__ == '__main__':
    app.run(port=90,host='0.0.0.0')
