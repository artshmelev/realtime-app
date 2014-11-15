import random

class Player(object):
    def __init__(self, channel, name='test'):
        self.channel = channel
        self.name = name
        

class Game(object):
    def __init__(self, player1, player2):
        self.ps = [player1, player2]
        self.tasks0 = []
        self.tasks1 = []
        self.score = [0, 0]


class GamePool(object):
    def __init__(self):
        self.games = []
        self.players = []
        self.waiting_players = []
        
    def append(self, player):
        self.players.append(player)
        if len(self.waiting_players) == 0:
            self.waiting_players.append(player)
            return (None, None)
        else:
            partner = self.waiting_players.pop() 
            self.games.append(Game(player, partner))
            return (player, partner)
        
    def remove(self, player):
        try:
            self.players.remove(player)
        except ValueError:
            pass
        try:
            self.waiting_players.remove(player)
        except ValueError:
            pass
        try:
            self.games.remove(find_game(player))
        except ValueError:
            pass
        
    def find_game(self, player):
        for g in self.games:
            if player in g.ps:
                return g
        return None
    
    def find_player(self, channel):
        for p in self.players:
            if p.channel == channel:
                return p
        return None
    
    
class Task(object):
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        if difficulty == 1:
            self.text, self.answer = self.gen_simple()
    
    def gen_simple(self):
        a1 = random.randint(0, 50)
        a2 = self.get_rand_sign()
        a3 = random.randint(0, 50)
        if a2 == '+':
            ans = str(a1 + a3)
        elif a2 == '-':
            ans = str(a1 - a3)
        return (str(a1) + a2 + str(a3), ans)
        
    
    def get_rand_sign(self):
        r = random.randint(0, 1)
        if r == 0:
            return '+'
        else:
            return '-'
        
    