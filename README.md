# cardpacks

```py

f = Deck() #Standard, uses standard Playing Card pack
f = Deck(jokers=False) #standard, without joker cards. 
#we can pass arbitrary values to the deck contstructor class.

#Also included is other packs (limited for now, more to come)

f = Deck(pack=FrenchStrippedPlayingPack) #0-9 numbered cards only
# Also available is TarotNouveauPack and TarotArcanaPack

# Once you have a deck, you can

f.shuffle()

#and

card = f.pull()
# card is now a randomly drawn card from the deck, it has various values based on the pack itself
# But the default packs try to be consistent, they have a .name, .value, 
#and when represented as string, they show a format of "the VALUE of CLASS" or something similar.
```

Also work-in-progress is a little system of making text-based card games.
```py
# To try the default Blackjack game.
import cardpacks

game = cardpacks.CGBlackjack() #create the game state

game.create("Kai") #starts a new game, blackjack takes an argument for the players name
#this is used in the text output, and also as a check for interfaces
#for example, if this is implemented in a discord bot
#it can be used as a way to know which discord user the game belongs to

print(game.players) #our blackjack example has 2 players

game.clr() #clr prints the message buffer. in this case, it'll show the "startup" messages
game.loop("Kai") #starts a CLI loop to play, argument is the name of the player in sent commands

# to implement custom interfaces, instead of using loop()
# you would run

game.execute("Kai", "hit")
# which sends a "hit" command to the game state under the name of Kai
# All the games in this system run on a command system, which can be arbitrarily added by the state
# And after every execute, you can run .clr() to grab the message output
```

It uses a modular system, so the game state can be modified at will.
```py
import cardpacks

def send(message):
  discord.webhooks.send(message)
  
game = cardpacks.CGBlackjack()
game.addHook('turn', send) #makes the game run send every turn
game.create()
game.clr()
game.loop()

"""
Other hooks include:

_restart : Hook that handles what happens when the game is over and can be restarted
Runs when the `new` command is issued, should point to a function that re-initializes the state.
_exit : Handles what happens when the `q` command is issued.
In the CLI loop, it runs quit(), but if you're plugging it in to another interface, maybe do something else.
exit : Handles what happens when the "game state" ends, e.i. when someone wins or loses.
pre_turn : Runs before every command is run.
post_turn : Runs after every command is run.
player_0_wins : Runs when a player wins, number should be whichever player ID wins.
no_player_wins : Runs in the case of a draw

But, hooks are arbitrary keys, and you can add your own names with
game.addHook('cheat', callable_function)
and then trigger them in code with:
game.hook('cheat')

See the code for other example functions that can be used to modify the game state.
"""
```
