import itertools
import random

class TarotNouveauCard:
	def __init__(self, *, number, icon, theme, group):
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
			'the fool',
			'the magician',
			'the high priestess',
			'the empress', 
			'the emperer',
			'the hierophant',
			'the lovers',
			'chariot',
			'justice',
			'hermit',
			'wheel of fortune',
			'strength',
			'the hanged man',
			'death',
			'temperance',
			'the devil',
			'the tower',
			'the star',
			'the moon',
			'the sun',
			'judgement',
			'the world'
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
			return f"{self.name} of {self.suit}s"
		else:
			return self.name

class TarotArcanaPack:
	@staticmethod
	def get():
		deck = []
		for i in range(0, 14):
			deck.append(MinorArcanaTarotCard('swords', i))
			deck.append(MinorArcanaTarotCard('cups', i))
			deck.append(MinorArcanaTarotCard('pentacles', i))
			deck.append(MinorArcanaTarotCard('wands', i))
		for i in range(0, 22):
			deck.append(MajorArcanaTarotCard(i))
		return deck
	
class TarotNouveauPack:
	@staticmethod
	def get():
		deck = []
		deck.append(TarotNouveauCard(number=1, icon="🃡", theme="individual", group="folly"))
		deck.append(TarotNouveauCard(number=2, icon="🃢", theme="childhood", group="the four ages"))
		deck.append(TarotNouveauCard(number=3, icon="🃣", theme="youth", group="the four ages"))
		deck.append(TarotNouveauCard(number=4, icon="🃤", theme="maturity", group="the four ages"))
		deck.append(TarotNouveauCard(number=5, icon="🃥", theme="old age", group="the four ages"))
		deck.append(TarotNouveauCard(number=6, icon="🃦", theme="morning", group="the four times of day"))
		deck.append(TarotNouveauCard(number=7, icon="🃧", theme="afternoon", group="the four times of day"))
		deck.append(TarotNouveauCard(number=8, icon="🃨", theme="evening", group="the four times of day"))
		deck.append(TarotNouveauCard(number=9, icon="🃩", theme="night", group="the four times of day"))
		deck.append(TarotNouveauCard(number=10, icon="🃪", theme="earth", group="the four elements"))
		deck.append(TarotNouveauCard(number=10, icon="🃪", theme="air", group="the four elements"))		
		deck.append(TarotNouveauCard(number=11, icon="🃫", theme="water", group="the four elements"))
		deck.append(TarotNouveauCard(number=11, icon="🃫", theme="fire", group="the four elements"))
		deck.append(TarotNouveauCard(number=12, icon="🃬", theme="dance", group="the four leisures"))
		deck.append(TarotNouveauCard(number=13, icon="🃭", theme="shopping", group="the four leisures"))
		deck.append(TarotNouveauCard(number=14, icon="🃮", theme="open air", group="the four leisures"))
		deck.append(TarotNouveauCard(number=15, icon="🃯", theme="visual arts", group="the four leisures"))
		deck.append(TarotNouveauCard(number=16, icon="🃰", theme="spring", group="the four seasons"))
		deck.append(TarotNouveauCard(number=17, icon="🃱", theme="summer", group="the four seasons"))
		deck.append(TarotNouveauCard(number=18, icon="🃲", theme="autumn", group="the four seasons"))
		deck.append(TarotNouveauCard(number=19, icon="🃳", theme="winter", group="the four seasons"))
		deck.append(TarotNouveauCard(number=20, icon="🃴", theme="the game", group="the game"))
		deck.append(TarotNouveauCard(number=21, icon="🃵", theme="collective", group="folly"))
		return deck
	
class StandardPlayingPack:
	@staticmethod
	def get():
		deck = []
		for i in range(0, 12):
			deck.append(PlayingCard(suit='heart', icon='♥', value=i))
			deck.append(PlayingCard(suit='spade', icon='♠', value=i))
			deck.append(PlayingCard(suit='diamond', icon='♦', value=i))
			deck.append(PlayingCard(suit='club', icon='♣', value=i))
		
		for i in range(0, 6):
			deck.append(PlayingCard(value='joker'))
			
		return deck
	
class FrenchStrippedPlayingPack:
	@staticmethod
	def get():
		deck = []
		for i in range(0, 9):
			deck.append(PlayingCard('heart', '♥', i))
			deck.append(PlayingCard('spade', '♠', i))
			deck.append(PlayingCard('diamond', '♦', i))
			deck.append(PlayingCard('club', '♣', i))

		return deck	
	
class Deck:
	def __init__(self, *, pack=StandardPlayingPack):
		if type(pack) == list:
			self.cards = pack
		else:
			self.cards = pack.get()
	
	def shuffle(self, newpack = None):
		if newpack:
			if type(newpack) == list:
				self.cards = newpack
			else:
				self.cards = newpack.get()

		random.shuffle(self.cards)
		return self.cards
	
	def pull(self, shuffle=True):
		if shuffle:
			self.shuffle()
		self.new_card = self.cards[0]
		del self.cards[0]
		return self.new_card
