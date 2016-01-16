#! /usr/bin/env python

import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template
from pprint import pprint

app = Flask(__name__)

ws_list = set()

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/websocket")
def echo():

    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        ws_list.add(ws)

        print "enter:", len(ws_list), request.environ["REMOTE_ADDR"], request.environ["REMOTE_PORT"]

        while True:
            message = ws.receive()
            if message is None:
                break

            remove = set()
            for s in ws_list:
                try:
                    s.send(message)
                except Exception:
                    remove.add(s)

            for s in remove:
                ws_list.remove(s)

            pprint(message)

        print "exit:", request.environ["REMOTE_ADDR"], request.environ["REMOTE_PORT"]
        ws_list.remove(ws)
    return

if __name__ == "__main__":
    server = pywsgi.WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
