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
                self.send(json.dumps({'action': 'startgame',
                                      'side': 'left'}))
                p2.channel.send(json.dumps({'action': 'startgame',
                                            'side': 'right'}))
                
        elif data['action'] == 'ready':
            g = pool.find_game(pool.find_player(self))
            
            if len(g.tasks0) < 3:
                g.tasks0.append(Task())
            if len(g.tasks1) < 3:
                g.tasks1.append(Task())
                
            self.send(json.dumps({'action': 'tasking',
                                  'score0': g.score[0],
                                  'score1': g.score[1],
                                  'tasks0': [t.text for t in g.tasks0],
                                  'tasks1': [t.text for t in g.tasks1]}))
            
        elif data['action'] == 'answer':
            player = pool.find_player(self)
            g = pool.find_game(player)
            
            if player == g.ps[0]:
                for t in g.tasks0:
                    if t.answer == data['answer']:
                        self.send(json.dumps({'action': 'result',
                                              'result': 'ok'}))
                        g.tasks0.remove(t)
            
            elif player == g.ps[1]:
                for t in g.tasks1:
                    if t.answer == data['answer']:
                        self.send(json.dumps({'action': 'result',
                                              'result': 'ok'}))
                        g.tasks1.remove(t)
        
        elif data['action'] == 'gameover':
            pool.remove(pool.find_player(self))
            self.send(json.dumps({'action': 'startpage'}))
        
    def on_close(self):
        print 'close sock'
        pool.remove(pool.find_player(self))
        self.clients.remove(self)


if __name__ == '__main__':
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    
    app = web.Application(
        [(r'/', IndexHandler)] + EchoRouter.urls,
    **settings)
    app.listen(8888)
    ioloop.IOLoop.instance().start()
