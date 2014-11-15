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
    
    def on_open(self, info):
        print 'open sock'
        self.clients.add(self)
        
    def on_message(self, msg):
        data = json.loads(msg)
        
        if data['action'] == 'connecting':
            self.send(json.dumps({'action': 'startpage'}))
        elif data['action'] == 'disconnecting':
            pass
        elif data['action'] == 'playgame':
            p1, p2 = pool.append(Player(self))
            if p1 == None:
                self.send(json.dumps({'action': 'waiting'}))
            else:
                self.send(json.dumps({'action': 'startgame'}))
                p2.channel.send(json.dumps({'action': 'startgame'}))
                
        elif data['action'] == 'ready':
            pass
        elif data['action'] == 'answer':
            pass
        elif data['action'] == 'gameover':
            pass
        
    def on_close(self):
        print 'close sock'
        self.clients.remove(self)
        pool.remove(Player(self))


if __name__ == '__main__':
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    
    app = web.Application(
        [(r'/', IndexHandler)] + EchoRouter.urls,
    **settings)
    app.listen(8888)
    ioloop.IOLoop.instance().start()
