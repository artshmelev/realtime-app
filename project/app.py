import os, json
from tornado import ioloop, web
from sockjs.tornado import SockJSRouter, SockJSConnection

from game_structs import *

settings = {
    'static_path': os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'static'),
    'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
    'login_url': '/login',
}

pool = GamePool()

class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    

class IndexHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)
        
        
class LoginHandler(BaseHandler):
    def get(self):
        self.render('auth.html')
        
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        #if username == 'test' and password == 'test' or \
            #username == 'test1' and password == 'test1':
        self.set_secure_cookie('user', username)
        self.redirect('/')
        '''else:
            wrong = self.get_secure_cookie('wrong')
            if wrong == False or wrong == None:
                wrong = 0
            self.set_secure_cookie('wrong', str(int(wrong) + 1))
            self.write('Wrong username/password. Try again.')'''
            
        
        
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))    
        

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
            if g == None:
                self.send(json.dumps({'action': 'startpage'}))
                return
            
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
        player = pool.find_player(self)
        partner = pool.find_partner(player)
        if (partner != None):
            partner.channel.send(json.dumps({'action': 'startpage'}))
        pool.remove(player)
        self.clients.remove(self)


if __name__ == '__main__':
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    
    app = web.Application(
        [(r'/', IndexHandler),
         (r'/login', LoginHandler),
         (r'/logout', LogoutHandler)] + EchoRouter.urls,
    **settings)
    app.listen(8888, address='0.0.0.0')
    ioloop.IOLoop.instance().start()
