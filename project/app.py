import os, json
from tornado import ioloop, web
from sockjs.tornado import SockJSRouter, SockJSConnection
import psycopg2

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
        username, id = self.get_current_user().split('|')
        
        db = psycopg2.connect("host='localhost' dbname='ra_db' user='test_user' password='sOmq3cPa'")
        c = db.cursor()
        query0 = '''SELECT username, rating FROM ra_users ORDER BY rating DESC
                    LIMIT 10;'''
        c.execute(query0)
        data = c.fetchall()
        
        query1 = '''SELECT username FROM ra_users WHERE username = 
                    '%(username)s';''' % {'username': username}
        c.execute(query1)
        data1 = c.fetchall()
        if len(data1) == 0:
            query2 = '''INSERT INTO ra_users(id, username, num_games, rating)
                        VALUES ('%(id)s', '%(username)s', '%(num_games)s',
                                '%(rating)s');''' % {'id': int(id),
                                                     'username': username,
                                                     'num_games': 0,
                                                     'rating': 0}
            c.execute(query2)
            db.commit()
        
        c.close()
        db.close()
        self.render('index.html', user=username, data=data)
        
        
class LoginHandler(BaseHandler):
    def get(self):
        self.render('auth.html')
        
    def post(self):
        type = self.get_argument('type')
        username = self.get_argument('username')
        password = self.get_argument('password')
        if type == 'form' and username == 'test' and password == '1234' or \
           type == 'vk':
            self.set_secure_cookie('user', username + '|' + password)
            self.redirect('/')
        else:
            wrong = self.get_secure_cookie('wrong')
            if wrong == False or wrong == None:
                wrong = 0
            self.set_secure_cookie('wrong', str(int(wrong) + 1))
            self.write('Wrong username/password. Try again.')
        
        
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
            self.send(json.dumps({ 'action': 'startpage' }))
            
            
        elif data['action'] == 'disconnecting':
            pass
        
        
        elif data['action'] == 'playgame':
            p1, p2 = pool.append(Player(self, data['username']))
            if p1 == None:
                self.send(json.dumps({ 'action': 'waiting' }))
            else:
                self.send(json.dumps({ 'action': 'startgame',
                                       'side': 'left',
                                       'partner': p2.name }))
                p2.channel.send(json.dumps({ 'action': 'startgame',
                                             'side': 'right',
                                             'partner': p1.name }))
                
                
        elif data['action'] == 'ready':
            g = pool.find_game(pool.find_player(self))
            if g == None:
                self.send(json.dumps({ 'action': 'startpage' }))
                return
            
            if len(g.tasks0) < 4:
                g.tasks0.append(Task())
            if len(g.tasks1) < 4:
                g.tasks1.append(Task())
                
            self.send(json.dumps({ 'action': 'tasking',
                                   'score0': g.score[0],
                                   'score1': g.score[1],
                                   'tasks0': [t.text for t in g.tasks0],
                                   'tasks1': [t.text for t in g.tasks1],
                                   'xs0':    [t.x for t in g.tasks0],
                                   'ys0':    [t.y for t in g.tasks0],
                                   'xs1':    [t.x for t in g.tasks1],
                                   'ys1':    [t.y for t in g.tasks1] }))
            
            
        elif data['action'] == 'answer':
            player = pool.find_player(self)
            g = pool.find_game(player)
            
            if player == g.ps[0]:
                for t in g.tasks0:
                    if t.answer == data['answer']:
                        g.score[0] += 10
                        self.send(json.dumps({ 'action': 'result',
                                               'result': 'ok' }))
                        g.tasks0.remove(t)
            
            elif player == g.ps[1]:
                for t in g.tasks1:
                    if t.answer == data['answer']:
                        g.score[1] += 10
                        self.send(json.dumps({ 'action': 'result',
                                               'result': 'ok' }))
                        g.tasks1.remove(t)
        
        
        elif data['action'] == 'gameover':
            player = pool.find_player(self)
            g = pool.find_game(player)
            if g != None:
                win = 0
                if data['win_left'] == 1 and g.ps[0] == player or \
                   data['win_left'] == 0 and g.ps[1] == player:
                    win = 1
                self.send(json.dumps({ 'action': 'displayscore',
                                       'score': str(g.score[0]) + '-' + \
                                                str(g.score[1]),
                                       'win': win }))
                partner = pool.find_partner(player)
                partner.channel.send(json.dumps({
                                       'action': 'displayscore',
                                       'score': str(g.score[0]) + '-' + \
                                                str(g.score[1]),
                                       'win': win^1 }))
                
                db = psycopg2.connect("host='localhost' dbname='ra_db' user='test_user' password='sOmq3cPa'")
                c = db.cursor()
                if win == 1:
                    query0 = '''UPDATE ra_users SET num_games = num_games + 1,
                                rating = rating + '%(diff)d' WHERE username = 
                                '%(name)s';'''%{'diff': abs(g.score[0]-g.score[1]),
                                                'name': player.name}
                    query1 = '''UPDATE ra_users SET num_games = num_games + 1
                                WHERE username='%(name)s';'''% {'name': partner.name}
                else:
                    query0 = '''UPDATE ra_users SET num_games = num_games + 1,
                                rating = rating + '%(diff)d' WHERE username = 
                                '%(name)s';'''%{'diff': abs(g.score[0]-g.score[1]),
                                                'name': partner.name}
                    query1 = '''UPDATE ra_users SET num_games = num_games + 1
                                WHERE username='%(name)s';'''% {'name': player.name}          
                c.execute(query0)
                c.execute(query1)
                db.commit()
                c.close()
                db.close()
                
                
        elif data['action'] == 'restart':
            pool.remove(pool.find_player(self))
            self.send(json.dumps({ 'action': 'startpage' }))
        
    def on_close(self):
        print 'close sock'
        player = pool.find_player(self)
        partner = pool.find_partner(player)
        if (partner != None):
            partner.channel.send(json.dumps({ 'action': 'startpage' }))
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
