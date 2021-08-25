###
# WateringServer 
# A control program with websocket.
# version: v1.1.1
from route.index import here_index
from common.welcome import Welcome
from common.properties import port,address
from flask import Flask, render_template
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from libs.MyWebSocket import WebSocket
from tornado.ioloop import IOLoop

app = Flask(__name__)

app.register_blueprint(here_index, url_prefix='')


def index():
    return render_template('index.html')


if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ])
    server.listen(port, address=address)
    Welcome()
    IOLoop.instance().start()
