import gevent
from flask import Flask
from flask_sockets import Sockets
from  RedisListener import PubSubListener
pslistener = PubSubListener()

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/echo')
def echo_socket(ws):
    pslistener.register(ws)

    while not ws.closed:
        gevent.sleep(0.1)

@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    print("Started")
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()