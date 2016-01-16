import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
                                                                                                                        
@app.route('/echo')
def echo():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            src = ws.receive()
            if src is None:
                print "none"
                break
            ws.send(src)
    return

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
