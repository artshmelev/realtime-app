import os, json
from tornado import ioloop, web
from sockjs.tornado import SockJSRouter, SockJSConnection

from game_structs import *

settings = {
    'static_path': os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'static')
}

pool = GamePool()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')
        

class EchoConnection(SockJSConnection):
    clients = set()
    
    def on_open(self):
        print 'open sock'
        clients.add(self)
        
    def on_message(self, msg):
        data = json.loads(msg)
        
        if data['action'] == 'connecting':
            pass
        elif data['action'] == 'disconnecting':
            pass
        elif data['action'] == 'playgame':
            pass
        elif data['action'] == 'ready':
            pass
        elif data['action'] == 'answer':
            pass
        elif data['action'] == 'gameover':
            pass 
        self.send(msg)
        
    def on_close(self):
        print 'close sock'
        clients.remove(self)
        pool.remove(Player(self))


if __name__ == '__main__':
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    
    app = web.Application(
        [(r'/', IndexHandler)] + EchoRouter.urls,
    **settings)
    app.listen(8888)
    ioloop.IOLoop.instance().start()
