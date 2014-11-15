
class Player(object):
    def __init__(self, channel, name='test', game=None):
        self.channel = channel
        self.name = name
        self.game = game
        

class Game(object):
    def __init__(self, player1, player2):
        self.ps = [player1, player2]


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
        self.players.remove(player)
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
    
    
class Task(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
    