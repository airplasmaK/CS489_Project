from logging import debug
from flask import Flask, render_template, request, jsonify, make_response
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/', methods = ["GET","POST"])
def index():
    urls = request.form.get('urls').split(',')
    links = []
    for p in urls:
        try:
            r = requests.head(p)
            status = r.status_code
            links.append([p,status])
        except requests.ConnectionError:
            status = -1 #status 없음
            links.append([p,status])

    print(links)
    return build_actual_response(jsonify(links)),200  # serialize and use JSON headers

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    print("hihi")
    app.run(host = '127.0.0.1', port = 1024, debug = True)