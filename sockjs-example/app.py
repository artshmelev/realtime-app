import os
from tornado import ioloop, web
from sockjs.tornado import SockJSRouter, SockJSConnection


settings = {
    'static_path': os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'static')
}

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')


class EchoConnection(SockJSConnection):
    def on_message(self, msg):
        print msg
        self.send(msg)


if __name__ == '__main__':
    EchoRouter = SockJSRouter(EchoConnection, '/echo')

    app = web.Application(
        [(r'/', IndexHandler)] + EchoRouter.urls,
    **settings)
    app.listen(8888)
    ioloop.IOLoop.instance().start()

