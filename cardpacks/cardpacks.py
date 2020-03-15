import itertools
import random
import copy
import humanfriendly

class CardGame:
    def __init__(self):
        self.deck = None
        self.hooks = {}
        self.commands = {}
        self.vars = {}
        self.messageBuffer = []
        self.players = []
        self.help_files = {}
        self.addHook('exit', self.defExitHook)

    def defExitHook(self):
        self.message("Game over.")
        self.players = []
        self.svar('playing', False)
        
    def svar(self, key, val):
        self.vars[key.lower()] = val

    def gvar(self, key):
        return self.vars.get(key.lower())

    def player(self, index):
        try:
            return self.players[index]
        except IndexError:
            return None

    def fillAllHands(self):
        for p in self.players:
            self.fillHand(p)
            
    def fillHand(self, p):
        while len(p['hand']) < p['maxhand']:
            p['hand'].append(self.deck.pull())
            
    def clr(self, p=True):
        r = self.output(p)
        self.messageBuffer = []
        return r
    
    def output(self, printIt=True):
        if printIt:
            for item in self.messageBuffer:
                print(item)

        return copy.copy(self.messageBuffer)
    
    def getHelp(self, topic):
        if self.help_files.get(topic):
            self.message(self.help_files[topic])
            return
        
        for item in self.help_files.keys():
            if topic.lower() in item.lower():
                self.message(self.help_files[item])
                
    def addPlayer(self, **new):
        p = {}
        p.update({"name": "DEFAULT", "cpu": False, 'hand': [], 'maxhand': 7})
        p.update(new)
        self.players.append(p.copy())

    def message(self, text):
        self.messageBuffer.append(text)
        self.hook('message', text=text)
        
    def addCommand(self, name, fn):
        self.commands[name] = fn

    def loop(self):
        self.addHook('_exit', lambda: quit())
        
        while True:
            self.execute(input("> "))
            self.clr()

    def showHand(self, index):
        p = self.player(index)
        f = [i.__repr__() for i in p['hand']]
        return humanfriendly.text.concatenate(f)

    def getHandTotal(self, index):
        i = 0
        for card in self.player(index)['hand']:
            if card.value > 10:
                i += 10
            else:
                i += card.value
        return i
    
    def execute(self, command):
        args = []
        if len(command.split()) > 1:
            args = command.split()[1:]
            command = command.split()[0]

        if command == "q":
            self.hook('_exit')
            return
        
        if command == "new" and not self.gvar('playing'):
            print(args)
            if len(args) == 1:
                self.hook('_restart', name=args[0])
            else:
                self.hook('_restart')
            return
        
        if not self.gvar('playing'):
            self.message("Game is over.")
            if self.hasHook('_restart'):
                self.message("Enter `new` to restart.")
            if self.hasHook('_exit'):
                self.message("Enter `q` to exit the interface.")
            return
        
        if self.commands.get(command):
            self.hook('turn')
            return self.commands[command](*args)
        
        
    def addHook(self, name, fn):
        self.hooks[name] = fn

    def unhook(self, name):
        if self.hooks.get(name):
            del self.hooks[name]
            
    def hasHook(self, name):
        if self.hooks.get(name):
            return True
        return False
            
    def hook(self, hook_name, *args, **kargs):
        if self.hooks.get(hook_name):
            self.hooks[hook_name](*args, **kargs)


class CGBlackjack(CardGame):
    def __init__(self):
        super().__init__()
        self.addHook('_restart', self._initBlackjack)
        
        self.addCommand('hit', self.hit)
        self.addCommand('stand', self.stand)
        self.addCommand('quit', lambda: self.hook('exit'))
        self.addCommand('restart', lambda: self.hook('_restart'))

    def checkState(self, finalize=False):
        p = self.getHandTotal(0)
        h = self.getHandTotal(1)
                
        if p > 21:
            self.message("You went bust!")
            self.hook(f'player_1_win')
            self.hook('exit')
            
        elif h > 21:
            self.message("House went bust!")
            self.hook(f'player_0_win')
            self.hook('exit')
            
        elif h > 21 and p > 21:
            self.message("Both went bust!!?")
            self.hook('exit')

        elif h > p and finalize:
            self.message("House is closer to 21, house wins.")
            self.hook(f'player_1_win')
            self.hook('exit')
            
        elif h < p and finalize:
            self.message("Player is closer to 21, Player wins.")
            self.hook(f'player_0_win')
            self.hook('exit')
            
        elif h == p and finalize:
            self.message("It's a draw.")
            self.hook('exit')
            
    def hit(self, *args, **kargs):
        new = self.deck.draw()
        self.player(0)['hand'].append(new)
        self.message(f"You draw {new}")
        self.message(f"Your hand is... {self.showHand(0)} - {self.getHandTotal(0)}")
        self.checkState()
        
    def stand(self, *args, **kargs):
        self.message(f"Your hand is... {self.showHand(0)} - Player finishes at {self.getHandTotal(0)}.")
        self.message(f"House starts from... {self.showHand(1)} - {self.getHandTotal(1)}")
        while self.gvar('playing'):
            self.runHouse()
        
    def runHouse(self):
        if self.getHandTotal(1) < 10:
            new = self.deck.draw()
            self.player(1)['hand'].append(new)
            self.message(f"House draws {new} {self.getHandTotal(1)}") 
            self.checkState()
            
        elif self.getHandTotal(1) >= 10 and self.getHandTotal(1) < 13:
            if random.random() < 0.8:
                new = self.deck.draw()
                self.player(1)['hand'].append(new)
                self.message(f"House draws {new} {self.getHandTotal(1)}") 
                self.checkState()
            else:
                self.message(f"House Holds at {self.getHandTotal(1)}") 
                self.checkState(True)
                
        elif self.getHandTotal(1) >= 13 and self.getHandTotal(1) < 16:
             if random.random() < 0.5:
                new = self.deck.draw()
                self.player(1)['hand'].append(new)
                self.message(f"House draws {new} {self.getHandTotal(1)}") 
                self.checkState()
             else:
                self.message(f"House Holds at {self.getHandTotal(1)}") 
                self.checkState(True)
        elif self.getHandTotal(1) >= 16 and self.getHandTotal(1) < 18:
             if random.random() < 0.2:
                new = self.deck.draw()
                self.player(1)['hand'].append(new)
                self.message(f"House draws {new} {self.getHandTotal(1)}") 
                self.checkState()
             else:
                self.message(f"House Holds at {self.getHandTotal(1)}")  
                self.checkState(True)
        else:
            self.message(f"House Holds at {self.getHandTotal(1)}") 
            self.checkState(True)
        
    def create(self, name="Player"):
        self._initBlackjack(name)
        self.hook("init", name=name)

    def _initBlackjack(self, name="Player"):
        self.svar('playing', True)
        self.svar('mode', 0)
        self.message("Blackjack started!")
        self.deck = Deck(jokers=False)
        self.deck.shuffle()
        self.addPlayer(name=name, maxhand=2)
        self.addPlayer(name="House", cpu=True, maxhand=2)
        self.fillAllHands()
        self.message(f"[{name}] Your hand is... {self.showHand(0)} - {self.getHandTotal(0)}")
        self.message(f"House holds... {self.showHand(1)}")
        
class TarotNouveauCard:
    def __init__(self, number, icon, theme, group):
        self.number = number
        self.icon = icon
        self.theme = theme
        self.group = group

    def __repr__(self):
        return f"{self.icon} #{self.number} {self.group}, {self.theme}"

class MajorArcanaTarotCard:
    def __init__(self, number):
        self.number = number
        self.faces = [
            "the fool",
            "the magician",
            "the high priestess",
            "the empress",
            "the emperer",
            "the hierophant",
            "the lovers",
            "chariot",
            "justice",
            "hermit",
            "wheel of fortune",
            "strength",
            "the hanged man",
            "death",
            "temperance",
            "the devil",
            "the tower",
            "the star",
            "the moon",
            "the sun",
            "judgement",
            "the world",
        ]
        self.name = self.faces[number]

    def __repr__(self):
        return f"#{self.number} {self.name}"

class MinorArcanaTarotCard:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

        if value == 0:
            self.name = "ace"

        elif value == 11:
            self.name = "princess"

        elif value == 12:
            self.name = "prince"

        elif value == 13:
            self.name = "queen"

        elif value == 14:
            self.name = "king"
        else:
            self.name = str(self.value)

    def __repr__(self):
        return f"{self.name} of {self.suit}"

class PlayingCard:
    def __init__(self, *, suit=None, icon=None, value=None):
        self.suit = suit
        self.icon = icon
        self.value = value

        if value == 0:
            self.name = "ace"

        elif value == 10:
            self.name = "jack"

        elif value == 11:
            self.name = "queen"

        elif value == 12:
            self.name = "king"

        else:
            self.name = str(self.value)

    def __repr__(self):
        if self.suit:
            return f"{self.name} of {self.icon} {self.suit}s"
        else:
            return self.name

class TarotArcanaPack:
    @staticmethod
    def get(*args, **kargs):
        deck = []
        for i in range(0, 14):
            deck.append(MinorArcanaTarotCard("swords", i))
            deck.append(MinorArcanaTarotCard("cups", i))
            deck.append(MinorArcanaTarotCard("pentacles", i))
            deck.append(MinorArcanaTarotCard("wands", i))
        for i in range(0, 22):
            deck.append(MajorArcanaTarotCard(i))
        return deck

class TarotNouveauPack:
    @staticmethod
    def get():
        deck = []
        deck.append(
            TarotNouveauCard(number=1, icon="🃡", theme="individual", group="folly")
        )
        deck.append(
            TarotNouveauCard(
                number=2, icon="🃢", theme="childhood", group="the four ages"
            )
        )
        deck.append(
            TarotNouveauCard(number=3, icon="🃣", theme="youth", group="the four ages")
        )
        deck.append(
            TarotNouveauCard(
                number=4, icon="🃤", theme="maturity", group="the four ages"
            )
        )
        deck.append(
            TarotNouveauCard(number=5, icon="🃥", theme="old age", group="the four ages")
        )
        deck.append(
            TarotNouveauCard(
                number=6, icon="🃦", theme="morning", group="the four times of day"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=7, icon="🃧", theme="afternoon", group="the four times of day"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=8, icon="🃨", theme="evening", group="the four times of day"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=9, icon="🃩", theme="night", group="the four times of day"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=10, icon="🃪", theme="earth", group="the four elements"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=10, icon="🃪", theme="air", group="the four elements"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=11, icon="🃫", theme="water", group="the four elements"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=11, icon="🃫", theme="fire", group="the four elements"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=12, icon="🃬", theme="dance", group="the four leisures"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=13, icon="🃭", theme="shopping", group="the four leisures"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=14, icon="🃮", theme="open air", group="the four leisures"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=15, icon="🃯", theme="visual arts", group="the four leisures"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=16, icon="🃰", theme="spring", group="the four seasons"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=17, icon="🃱", theme="summer", group="the four seasons"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=18, icon="🃲", theme="autumn", group="the four seasons"
            )
        )
        deck.append(
            TarotNouveauCard(
                number=19, icon="🃳", theme="winter", group="the four seasons"
            )
        )
        deck.append(
            TarotNouveauCard(number=20, icon="🃴", theme="the game", group="the game")
        )
        deck.append(
            TarotNouveauCard(number=21, icon="🃵", theme="collective", group="folly")
        )
        return deck

class StandardPlayingPack:
    @staticmethod
    def get(*args, **kargs):
        deck = []
        for i in range(0, 12):
            deck.append(PlayingCard(suit="heart", icon="♥", value=i))
            deck.append(PlayingCard(suit="spade", icon="♠", value=i))
            deck.append(PlayingCard(suit="diamond", icon="♦", value=i))
            deck.append(PlayingCard(suit="club", icon="♣", value=i))

        if kargs.get('jokers'):
            for i in range(0, 6):
                deck.append(PlayingCard(value="joker"))

        return deck

class FrenchStrippedPlayingPack:
    @staticmethod
    def get(*args, **kargs):
        deck = []
        for i in range(0, 9):
            deck.append(PlayingCard("heart", "♥", i))
            deck.append(PlayingCard("spade", "♠", i))
            deck.append(PlayingCard("diamond", "♦", i))
            deck.append(PlayingCard("club", "♣", i))

        return deck

class Deck:
    def __init__(self, *, pack=StandardPlayingPack, **kargs):
        self.last_pull = None
        
        if type(pack) == list:
            self.cards = pack
        else:
            self.cards = pack.get(**kargs)

    def shuffle(self, newpack=None):
        if newpack:
            if type(newpack) == list:
                self.cards = newpack
            else:
                self.cards = newpack.get()

        random.shuffle(self.cards)
        return self.cards

    def draw(self, shuffle=False):
        return self.pull(shuffle)
    
    def pull(self, shuffle=False):
        if shuffle:
            self.shuffle()

        last_pull = self.cards[0]
        del self.cards[0]
        return last_pull
